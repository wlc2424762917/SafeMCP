import sys
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

from inspect_ai import eval
from inspect_ai.model import get_model, GenerateConfig

from src.inspect_evals.agentharm.agentharm import agentharm

# Setup model
model = get_model(
    "openai/gpt-4o",
    base_url="",
    api_key="",
    config=GenerateConfig(
        max_connections=1,
        max_retries=5,
        temperature=0.5,
    ),
)

# MCP defense model checkpoint path
model_path = ""

eval(
    agentharm(
        agent_kwargs={
            "use_mcp_defense": True,
            "mcp_defense_path": model_path,
            "tool_choice": "auto",
        }
    ),
    model=model,
    log_dir="logs/test_mcp_defense_harm_claude_test",
)
