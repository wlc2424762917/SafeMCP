export RAY_TMPDIR=/etc/ray_tmp_1
export WANDB_API_KEY=ea465cd55df1a8afbe8a7569d9bc9517ac94eed8
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

PYTHONUNBUFFERED=1 python3 -m verl.trainer.main_ppo \
 data.train_files=../data_SafeMCP/rl_guard_safety_tools_state_v5_wo_thought_safety_tools_reward_remove_none_remove_agentharm_injected_filter_9_new/train.parquet \
 data.val_files=../data_SafeMCP/rl_guard_safety_tools_state_v5_wo_thought_safety_tools_reward_remove_none_remove_agentharm_injected_filter_9_new/test.parquet \
 data.train_batch_size=128 \
 data.max_prompt_length=4200 \
 data.max_response_length=1024 \
 +data.apply_chat_template_kwargs.enable_thinking=False \
 ++data.truncation='middle' \
 actor_rollout_ref.model.path=./checkpoints/stage2_checkpoint/huggingface \
 actor_rollout_ref.actor.optim.lr=1e-6 \
 actor_rollout_ref.actor.ppo_mini_batch_size=96 \
 actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=6 \
 actor_rollout_ref.rollout.name=vllm \
 actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=12 \
 actor_rollout_ref.rollout.tensor_model_parallel_size=1 \
 actor_rollout_ref.rollout.gpu_memory_utilization=0.4 \
 actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=6 \
 critic.optim.lr=1e-5 \
 critic.model.path=./checkpoints/stage2_checkpoint/huggingface \
 critic.ppo_micro_batch_size_per_gpu=4 \
 algorithm.kl_ctrl.kl_coef=0.001 \
 trainer.logger=["console","wandb"] \
 trainer.val_before_train=False \
 trainer.n_gpus_per_node=8 \
 trainer.nnodes=1 \
 trainer.save_freq=100 \
 trainer.test_freq=50 \
 trainer.experiment_name=stage_3 \
 trainer.total_epochs=4 2>&1 | tee stage_3.log


 # 