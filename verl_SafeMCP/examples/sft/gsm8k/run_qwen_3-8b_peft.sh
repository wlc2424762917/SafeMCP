# Tested with 2 & 4 GPUs

set -x

if [ "$#" -lt 2 ]; then
    echo "[Warning] Missing arguments. Using default values."
    nproc_per_node=2
    save_path="./outputs/default"
else
    nproc_per_node=$1
    save_path=$2
    shift 2
fi

torchrun --standalone --nnodes=1 --nproc_per_node=$nproc_per_node \
     -m verl.trainer.fsdp_sft_trainer \
    data.train_files=/share/project/wlc/data/gsm8k/train.parquet \
    data.val_files=/share/project/wlc/data/gsm8k/test.parquet \
    data.prompt_key=extra_info \
    data.response_key=extra_info \
    optim.lr=1e-4 \
    data.prompt_dict_keys=['question'] \
    +data.response_dict_keys=['answer'] \
    data.micro_batch_size_per_gpu=4 \
    model.partial_pretrain=/share/project/shared/models/qwen/Qwen3-8B \
    trainer.default_local_dir=$save_path \
    trainer.project_name=gsm8k-sft \
    trainer.experiment_name=gsm8k-sft-qwen-2.5-0.5b-instruct \
    trainer.logger=console \
    trainer.total_epochs=1 $@ \
    model.lora_rank=32\
    model.lora_alpha=16 \
    model.target_modules=all-linear

    # Or you can do this:
    # model.target_modules=[q_proj,v_proj] \
