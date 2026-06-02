# SafeMCP: Proactive Power Regulation for LLM Agent Defense

This repository contains the official code for the paper **SafeMCP: Proactive Power Regulation for LLM Agent Defense via Environment-Grounded Look-Ahead Reasoning**. It includes the training and evaluation code for **SafeMCP**, a server-side defense plugin that constrains tool acquisition via predictive reasoning regarding future safety risks.

## Environment Setup

### Prerequisites

- Python 3.11+
- PyTorch 2.0+ with CUDA support
- OpenAI API key (for base agent models and LLM-based evaluation)

### Installation

```bash
# 1. Install ToolEmu evaluation
cd ToolEmu
pip install -e .

# Install PromptCoder (required by ToolEmu)
git clone https://github.com/dhh1995/PromptCoder.git
cd PromptCoder && pip install -e . && cd ..

# 2. Install Inspect Evals (for AgentHarm)
cd ../inspect_evals
pip install inspect-ai
pip install -e .

# 3. PowerSeeking dependencies (no separate install needed)
cd ../PowerSeeking
pip install openai transformers torch tqdm
```

### API Configuration

Set your OpenAI-compatible API credentials. For ToolEmu, create a `.env` file:

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1
```

For PowerSeeking and AgentHarm scripts, fill in `API_KEY` and `BASE_URL` / `base_url` directly in the run scripts.

### SafeMCP Defense Model

All evaluation scripts require a SafeMCP checkpoint path. Update `model_path` / `MCP_MODEL_PATH` in each script:

```python
model_path = "/path/to/safemcp_checkpoint"
```

## Directory Structure

```
SafeMCP/
├── verl_SafeMCP/         # RL training code (VERL-based PPO)
├── data_SafeMCP/         # Training data (Environment Grounding, SFT, RL)
├── ToolEmu/              # ToolEmu evaluation (safety & helpfulness)
├── inspect_evals/        # AgentHarm benchmark evaluation
├── PowerSeeking/         # PowerSeeking Bench evaluation
└── README.md
```

## Three-Stage Training Pipeline

### Stage 1: Combined Experience SFT

```bash
cd verl_SafeMCP
bash run_stage_1.sh [nproc_per_node] [save_path]
```

After training, merge LoRA weights (if needed):
```bash
python merge_lora_weights.py \
    --base_model_path ./checkpoints/stage1_checkpoint/huggingface \
    --output_path ./checkpoints/stage1_checkpoint_merged
```

### Stage 2: Forecasting & Reasoning SFT

```bash
bash run_stage_2.sh
```

### Stage 3: RL Training (PPO)

```bash
bash run_stage_3.sh
```

**Note**: Update checkpoint paths in each stage script according to your actual model paths.

## Evaluation

### ToolEmu (Safety & Helpfulness)

```bash
cd ToolEmu
python emulate_case_all.py

# Safety evaluation
python scripts/evaluate.py -inp ./dumps/notebook/res.jsonl -ev agent_safe --evaluator-model-name gpt-4o

# Helpfulness evaluation
python scripts/evaluate.py -inp ./dumps/notebook/res.jsonl -ev agent_help --evaluator-model-name gpt-4o
```

### AgentHarm (Harmful Tool-Calling Defense)

```bash
cd inspect_evals/agentharm_runs
python test_mcp_defense.py              # Harmful scenarios
python test_mcp_defense_benign.py       # Benign scenarios (utility)
```

### PowerSeeking Bench (Power Acquisition Mitigation)

```bash
cd PowerSeeking

# Generate trajectories with SafeMCP defense
python response_generation_async_openai_api_SYSTEM_PROMPT_testbed_MCP_DEFENSE_gpt-4o-mini.py

# Evaluate
python eval_testbed_res_mcp_defense.py
```

See each subdirectory's README for detailed usage.

## References

SafeMCP evaluations build on ToolEmu and AgentHarm. Please cite the original benchmarks when using the corresponding evaluation suites:

```bibtex
@inproceedings{ruan2024toolemu,
  title={Identifying the Risks of LM Agents with an LM-Emulated Sandbox},
  author={Ruan, Yangjun and Dong, Honghua and Wang, Andrew and Pitis, Silviu and Zhou, Yongchao and Ba, Jimmy and Dubois, Yann and Maddison, Chris J and Hashimoto, Tatsunori},
  booktitle={The Twelfth International Conference on Learning Representations},
  year={2024}
}

@article{andriushchenko2024agentharm,
  title={AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents},
  author={Andriushchenko, Maksym and Souly, Alexandra and Dziemian, Mateusz and Duenas, Derek and Lin, Maxwell and Wang, Justin and Hendrycks, Dan and Zou, Andy and Kolter, Zico and Fredrikson, Matt and Winsor, Eric and Wynne, Jerome and Gal, Yarin and Davies, Xander},
  journal={arXiv preprint arXiv:2410.09024},
  year={2024}
}

@misc{wang2026safemcpproactivepowerregulation,
      title={SafeMCP: Proactive Power Regulation for LLM Agent Defense via Environment-Grounded Look-Ahead Reasoning}, 
      author={Lichao Wang and Zhaoxing Ren and Tianzhuo Yang and Jiaming Ji and Chi Harold Liu and Yaodong Yang and Juntao Dai},
      year={2026},
      eprint={2606.01991},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2606.01991}, 
}
```
