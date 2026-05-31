#!/bin/bash
# ========== 自动Merge Checkpoint监控脚本 ==========
# 此脚本会长时间挂起，持续监控checkpoint目录
# 一旦检测到新的checkpoint就自动merge为HuggingFace格式

# ========== 配置参数 ==========
# checkpoint目录，根据实际情况修改
CHECKPOINT_DIR=${1:-"checkpoints/verl_examples/rlguard_safety_tools_qwen3-8b_from_sft_new_format_v5_combined_exp_ep_stch_sigmoid_all_old_wo_thought_redo_add_add_safe_sft_stch_1+1_critical_reward_v11_merge_full_real_redo_1"}

# 检查间隔（秒）
CHECK_INTERVAL=${2:-60}

# merge后端：fsdp 或 megatron
BACKEND=${3:-"fsdp"}

# merge成功后是否删除原始FSDP/Megatron碎片（true/false）
DELETE_SHARDS_AFTER_MERGE=${4:-"true"}

# 记录已处理checkpoint的文件
PROCESSED_FILE="${CHECKPOINT_DIR}/.merged_checkpoints"

# ========== 函数定义 ==========

# 检查checkpoint是否正在被写入（通过检查最近修改时间）
is_checkpoint_stable() {
    local ckpt_dir=$1
    local wait_time=30  # 等待30秒确认checkpoint写入完成
    
    # 获取目录最后修改时间
    local mtime1=$(stat -c %Y "$ckpt_dir" 2>/dev/null)
    sleep 5
    local mtime2=$(stat -c %Y "$ckpt_dir" 2>/dev/null)
    
    # 如果5秒内目录没有被修改，认为写入完成
    if [ "$mtime1" = "$mtime2" ]; then
        return 0
    else
        return 1
    fi
}

# 检查是否已经处理过
is_already_processed() {
    local step_name=$1
    if [ -f "$PROCESSED_FILE" ]; then
        grep -q "^${step_name}$" "$PROCESSED_FILE"
        return $?
    fi
    return 1
}

# 标记为已处理
mark_as_processed() {
    local step_name=$1
    echo "$step_name" >> "$PROCESSED_FILE"
}

# 删除FSDP/Megatron碎片文件，保留huggingface目录
delete_shards() {
    local step_dir=$1
    local target_dir="${step_dir}/huggingface"
    
    # 确保huggingface目录存在且有内容
    if [ ! -d "$target_dir" ] || [ -z "$(ls -A $target_dir 2>/dev/null)" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 警告: huggingface目录不存在或为空，跳过删除碎片"
        return 1
    fi
    
    # 计算删除前的大小
    local size_before=$(du -sh "$step_dir" 2>/dev/null | cut -f1)
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始删除FSDP碎片: $step_dir"
    
    # 删除除huggingface以外的所有文件和目录
    find "$step_dir" -mindepth 1 -maxdepth 1 ! -name 'huggingface' -exec rm -rf {} \;
    
    # 计算删除后的大小
    local size_after=$(du -sh "$step_dir" 2>/dev/null | cut -f1)
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 碎片删除完成: $size_before -> $size_after"
    return 0
}

# Merge单个checkpoint
merge_checkpoint() {
    local step_dir=$1
    local step_name=$2
    local target_dir="${step_dir}/huggingface"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始Merge: $step_dir"
    
    if [ "$BACKEND" = "megatron" ]; then
        python -m verl.model_merger merge \
            --backend megatron \
            --tie-word-embedding \
            --local_dir "$step_dir" \
            --target_dir "$target_dir"
    else
        python -m verl.model_merger merge \
            --backend fsdp \
            --local_dir "$step_dir" \
            --target_dir "$target_dir"
    fi
    
    if [ $? -eq 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Merge成功: $target_dir"
        mark_as_processed "$step_name"
        
        # 如果配置了删除碎片，则删除原始FSDP/Megatron碎片
        if [ "${DELETE_SHARDS_AFTER_MERGE}" = "true" ]; then
            delete_shards "$step_dir"
        fi
        
        return 0
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Merge失败: $step_dir"
        return 1
    fi
}

# ========== 主循环 ==========

echo "=========================================="
echo "自动Merge Checkpoint监控脚本"
echo "=========================================="
echo "监控目录: $CHECKPOINT_DIR"
echo "检查间隔: ${CHECK_INTERVAL}秒"
echo "Merge后端: $BACKEND"
echo "删除碎片: $DELETE_SHARDS_AFTER_MERGE"
echo "=========================================="
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始监控..."
echo ""

# 确保目录存在
mkdir -p "$CHECKPOINT_DIR"

# 创建已处理记录文件
touch "$PROCESSED_FILE"

while true; do
    # 检查是否存在global_step目录
    for step_dir in ${CHECKPOINT_DIR}/global_step_*/actor; do
        # 检查目录是否存在
        if [ ! -d "$step_dir" ]; then
            continue
        fi
        
        step_name=$(basename $(dirname $step_dir))
        target_dir="${step_dir}/huggingface"
        
        # 检查是否已经存在huggingface目录
        if [ -d "$target_dir" ]; then
            continue
        fi
        
        # 检查是否已经处理过（可能失败了）
        if is_already_processed "$step_name"; then
            continue
        fi
        
        # 检查checkpoint是否写入完成
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检测到新checkpoint: $step_name，等待写入完成..."
        
        if is_checkpoint_stable "$step_dir"; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checkpoint写入完成，开始merge..."
            merge_checkpoint "$step_dir" "$step_name"
        else
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checkpoint仍在写入中，跳过本次检查..."
        fi
    done
    
    # 等待下一次检查
    sleep $CHECK_INTERVAL
done

