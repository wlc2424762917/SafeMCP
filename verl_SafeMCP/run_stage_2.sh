# Tested with 2 & 4 GPUs

set -x

if [ "$#" -lt 2 ]; then
    echo "[Warning] Missing arguments. Using default values."
    nproc_per_node=8
    save_path="./checkpoints/stage2_checkpoint"

else
    nproc_per_node=$1
    save_path=$2
    shift 2
fi

torchrun --standalone --nnodes=1 --nproc_per_node=$nproc_per_node \
     -m verl.trainer.fsdp_sft_trainer \
    data.train_files=../data_SafeMCP/rl_guard_safety_tools_states_forecasting_reasoning_v11_2k_no_number_add_add_safe/train.parquet \
    data.val_files=../data_SafeMCP/rl_guard_safety_tools_states_forecasting_reasoning_v11_2k_no_number_add_add_safe/test.parquet \
    data.prompt_key=extra_info \
    data.response_key=extra_info \
    optim.lr=1e-5 \
    data.prompt_dict_keys=['question'] \
    +data.response_dict_keys=['answer'] \
    +data.apply_chat_template_kwargs.enable_thinking=False \
    data.max_length=6400 \
    data.micro_batch_size_per_gpu=2 \
    model.partial_pretrain=./checkpoints/stage1_checkpoint/huggingface \
    model.enable_gradient_checkpointing=True \
    trainer.default_local_dir=$save_path \
    trainer.project_name=stage_2 \
    trainer.experiment_name=stage_2 \
    trainer.logger=console \
    trainer.total_epochs=4 $@ \
    # model.lora_rank=32\
    # model.lora_alpha=16 \
    # model.target_modules=all-linear

