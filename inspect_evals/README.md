# AgentHarm Evaluation for SafeMCP

This directory evaluates SafeMCP on the [AgentHarm](https://github.com/AISI/inspect_evals) benchmark, testing whether SafeMCP can block harmful tool-calling behaviors while preserving utility on benign tasks.

## Setup

```bash
pip install inspect-ai
pip install -e .
```

Requires Python 3.11+, PyTorch, and Transformers (for loading the SafeMCP defense model).

## Running Evaluations

All run scripts are in `agentharm_runs/`. Before running, fill in the `model_path` (SafeMCP checkpoint) and API credentials in the script.

```bash
# Harmful scenarios (GPT-4o-mini as base agent + SafeMCP defense)
python agentharm_runs/test_mcp_defense.py

# Benign scenarios (utility preservation test)
python agentharm_runs/test_mcp_defense_benign.py

# Llama-3.1-8B as base agent
python agentharm_runs/test_mcp_defense_llama.py
python agentharm_runs/test_mcp_defense_benign_llama.py

# GPT-4o as base agent
python agentharm_runs/test_mcp_defense_claude_test.py
python agentharm_runs/test_mcp_defense_claude_test_benign.py

# Baseline (no defense)
python agentharm_runs/test_agentharm_harm_gpt_4o_mini.py
```

## Log Example

An example log of GPT-4o-mini with SafeMCP defense is provided in:

```
log_example/2025-12-16T17-24-00+08-00_agentharm_safemcp_4o_mini_readable_trajs/
├── trajs_readable.md      # Human-readable trajectory markdown
├── trajs_readable.json    # Structured JSON format
└── trajs_readable.jsonl   # JSONL format
```

Each trajectory entry contains: user instruction, agent tool calls, tool outputs, and SafeMCP intervention results (refusal or pass-through).

## Directory Structure

```
inspect_evals/
├── agentharm_runs/            # Evaluation run scripts
├── log_example/               # Example output logs
├── src/inspect_evals/         # Inspect Evals core library (includes agentharm task)
└── pyproject.toml             # Dependencies
```
