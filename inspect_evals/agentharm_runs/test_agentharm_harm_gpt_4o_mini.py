import sys
import os

from functools import wraps

from inspect_ai import eval
from inspect_ai.model import get_model, GenerateConfig, ModelOutput

from src.inspect_evals.agentharm.agentharm import agentharm

# Setup model
model = get_model(
    "openai/gpt-4o-mini",
    base_url="",
    api_key="",
    config=GenerateConfig(
        max_connections=1,
        max_retries=5,
        temperature=0.0,
    ),
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

eval(agentharm(), model=model)
