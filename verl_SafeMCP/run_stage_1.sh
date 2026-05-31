# Tested with 2 & 4 GPUs

set -x

if [ "$#" -lt 2 ]; then
    echo "[Warning] Missing arguments. Using default values."
    nproc_per_node=8
    save_path="./checkpoints/qwen3_combined_experience_tmp_1epoch_1e-5lr_lora_2ep_w_b2_all_old_data"
else
    nproc_per_node=$1
    save_path=$2
    shift 2
fi

torchrun --standalone --nnodes=1 --nproc_per_node=$nproc_per_node \
     -m verl.trainer.fsdp_sft_trainer \
    data.train_files=../data_SafeMCP/combined_experience_parquet_add_b2_w_all_old_data/train.parquet \
    data.val_files=../data_SafeMCP/combined_experience_parquet_add_b2_w_all_old_data/test.parquet \
    data.prompt_key=extra_info \
    data.response_key=extra_info \
    optim.lr=1e-5 \
    data.prompt_dict_keys=['question'] \
    +data.response_dict_keys=['answer'] \
    +data.apply_chat_template_kwargs.enable_thinking=False \
    ++data.truncation='left' \
    data.max_length=9600 \
    data.micro_batch_size_per_gpu=2 \
    model.partial_pretrain=./checkpoints/Qwen3-8B \
    model.enable_gradient_checkpointing=True \
    trainer.default_local_dir=$save_path \
    trainer.project_name=stage_1 \
    trainer.experiment_name=stage_1 \
    trainer.logger=console \
    trainer.total_epochs=2 $@ \
    model.lora_rank=32\
    model.lora_alpha=16 \
    model.target_modules=all-linear

