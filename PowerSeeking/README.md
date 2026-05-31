# PowerSeeking Bench Evaluation for SafeMCP

This directory evaluates whether LLM agents exhibit power-seeking behavior — acquiring capabilities beyond what is necessary for the task — and whether SafeMCP can effectively mitigate such risks.

## Quick Start

### 1. Generate Trajectories (Baseline)

```bash
# GPT-4o-mini
python response_generation_async_openai_api_SYSTEM_PROMPT_testbed_gpt-4o-mini.py

# Gemini-2.5-flash
python response_generation_async_openai_api_SYSTEM_PROMPT_testbed_gemini_2_5_flash.py

# Llama-3.1-8b
python response_generation_async_openai_api_SYSTEM_PROMPT_testbed_llama.py
```

### 2. Generate Trajectories (With SafeMCP Defense)

```bash
# GPT-4o-mini + SafeMCP
python response_generation_async_openai_api_SYSTEM_PROMPT_testbed_MCP_DEFENSE_gpt-4o-mini.py

# Gemini-2.5-flash + SafeMCP
python response_generation_async_openai_api_SYSTEM_PROMPT_testbed_MCP_DEFENSE_gemini.py

# Llama + SafeMCP
python response_generation_async_openai_api_SYSTEM_PROMPT_testbed_MCP_DEFENSE_llama.py
```

### 3. Evaluate Results

```bash
python eval_testbed_res_mcp_defense.py
# Update the input_file parameter in the script with your generated trajectory file
```

## Directory Structure

```
PowerSeeking/
├── response_generation_*_testbed_*.py         # Baseline trajectory generation
├── response_generation_*_MCP_DEFENSE_*.py     # Trajectory generation with SafeMCP
├── eval_testbed_res_mcp_defense.py            # Power-seeking evaluation (GPT-4o judge)
├── synthetic_tools/                           # Tool definitions (benign + harmful)
└── trajectories/                              # Generated trajectories and eval data
```
