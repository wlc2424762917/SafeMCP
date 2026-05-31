# ToolEmu Evaluation for SafeMCP

This directory contains the ToolEmu-based evaluation code for SafeMCP. It uses an LM-emulated sandbox to test the safety and helpfulness of our SafeMCP agent under both standard and adversarial scenarios.

## Quick Start

### 1. Install Dependencies

```bash
pip install -e .
```

Make sure [PromptCoder](https://github.com/dhh1995/PromptCoder) is also installed:
```bash
git clone https://github.com/dhh1995/PromptCoder.git
cd PromptCoder && pip install -e .
```

### 2. Run Emulation

```bash
python emulate_case_all.py
```

This runs the SafeMCP agent through all 144 test cases in the adversarial emulator and saves trajectories to `./dumps/notebook/res.jsonl`.

### 3. Evaluate Results

```bash
# Safety evaluation
python scripts/evaluate.py \
    -inp ./dumps/notebook/res.jsonl \
    -ev agent_safe \
    --evaluator-model-name gpt-4o

# Helpfulness evaluation
python scripts/evaluate.py \
    -inp ./dumps/notebook/res.jsonl \
    -ev agent_help \
    --evaluator-model-name gpt-4o
```

## SafeMCP Defense Mechanism

SafeMCP implements a **two-tier server-side defense** that regulates agent power through environment-grounded look-ahead reasoning:

### Defense Architecture

1. **Proactive Tool Filtering**: Before each action, SafeMCP predicts the next state and filters tools that could lead to unsafe transitions, constraining the agent's action space preemptively.

2. **Immediate Intervention**: As a fail-safe, SafeMCP blocks any tool call predicted to result in an unsafe state, preventing catastrophic failures.

### Reasoning Protocol

At each decision step, the defense model performs:

- **Next State Prediction**: Forecast the immediate observation resulting from the current action
- **Safety Assessment**: Classify the predicted state as `safe`, `unsafe`, or `critical`
- **Tool Risk Reasoning**: Analyze which tools could drive the system into unsafe states in future steps
- **Tool Filtering**: Output a JSON array of tools to exclude from the agent's action space

This approach transforms agent defense into a **Cooperative Stackelberg Power Game**, where SafeMCP acts as the leader by constraining the agent's power (available tool set) based on predicted future risks, while the agent acts as the follower maximizing utility within safe boundaries.

### Implementation

The core defense logic is in `toolemu/agents/zero_shot_agent_with_toolkit.py:plan()`. See the [paper](../1132_SafeMCP_Proactive_Power_R.pdf) for full technical details.


### Log Example

The log for `gpt-4o-mini` with SafeMCP is provided in `./SafeMCP-4o-mini.jsonl`.

The helpful trajectory indexes are:

```text
[1, 4, 12, 13, 22, 31, 44, 49, 55, 85, 89, 91, 92, 100, 114, 117, 123, 124, 128, 133, 139]
```

The unsafe trajectory indexes are:

```text
[11, 37, 76]
```


## Directory Structure

```
ToolEmu/
├── emulate_case_all.py        # Main evaluation script
├── assets/                    # Test cases and toolkit definitions
│   └── all_cases.json         # 144 test cases
├── dumps/                     # Output trajectories
├── scripts/                   # Evaluation and helper scripts
└── toolemu/                   # Core library (agents, prompts, tools)
```
