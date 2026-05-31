import sys
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

from functools import wraps

from inspect_ai import eval
from inspect_ai.model import get_model, GenerateConfig, ModelOutput

from src.inspect_evals.agentharm.agentharm import agentharm

# Setup model
model = get_model(
    "hf/local",
    model_path="meta-llama/Llama-3.1-8B-Instruct",
    device="auto",
)


def tool_id_fix_decorator(f):
    @wraps(f)
    async def wrapper(*args, **kwargs) -> ModelOutput:
        output = await f(*args, **kwargs)
        if (
            output.choices
            and output.choices[0].message.tool_calls
            and len(output.choices[0].message.tool_calls) > 1
        ):
            ids = [tc.id for tc in output.choices[0].message.tool_calls]
            if len(set(ids)) == 1:
                base_id = ids[0]
                for i, tool_call in enumerate(output.choices[0].message.tool_calls):
                    if i > 0:
                        tool_call.id = f"{base_id}_{i}"
        return output

    return wrapper


model.generate = tool_id_fix_decorator(model.generate)  # type: ignore

import transformers.generation.logits_process
original_temp_init = transformers.generation.logits_process.TemperatureLogitsWarper.__init__

def patched_temp_init(self, temperature):
    if temperature <= 0.0:
        temperature = 1e-6
    original_temp_init(self, temperature)

transformers.generation.logits_process.TemperatureLogitsWarper.__init__ = patched_temp_init

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
    log_dir="logs/test_mcp_defense_harm_llama",
)
