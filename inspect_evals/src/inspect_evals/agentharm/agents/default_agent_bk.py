from typing import Literal, Optional

from inspect_ai.solver import (
    Generate,
    Solver,
    TaskState,
    chain,
    generate,
    prompt_template,
    solver,
    system_message,
)
from inspect_ai.tool import ToolFunction
from inspect_ai._util.registry import registry_info

from inspect_evals.agentharm.prompts import get_jailbreak_template, get_system_prompt


@solver
def system_prompt_based_on_model(
    system_prompt_template: Optional[str],
    prompt_technique: Literal["standard", "cot", "react", "refusal"],
) -> Solver:
    """
    Solver that generates a system prompt based on the model name. The llama-3.1 models use a different default system prompt.

    Args:
        system_prompt_template (str): Name of system prompt in `prompts.py`.
        prompt_technique (Literal['standard', 'cot', 'react', 'refusal']): Prompting technique to apply to the system prompt.

    """

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        nonlocal system_prompt_template
        if system_prompt_template is None:
            model_name = state.model.name
            if "llama-3.1" in model_name.lower():
                system_prompt_template = "llama-3.1"
            else:
                system_prompt_template = "default"

        system_prompt = get_system_prompt(system_prompt_template, prompt_technique)
        if system_prompt != "":
            state = await system_message(system_prompt)(state, generate)
        return state

    return solve


@solver
def remove_one_tool() -> Solver:
    """Remove one tool from state.tools each time this solver runs."""
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        tool_names = [registry_info(tool).name for tool in state.tools]
        print(f"Available tools before removal: {tool_names}")
        # Available tools before removal: ['inspect_evals/transfer_money_crypto', 'inspect_evals/get_latest_emails', 'inspect_evals/transfer_money']
        
        if state.tools and len(state.tools) > 0:
            removed_name = registry_info(state.tools[0]).name
            print(f"Removing tool: {removed_name}")
            state.tools = state.tools[1:]
            
        remaining_names = [registry_info(tool).name for tool in state.tools]
        print(f"Remaining tools after removal: {remaining_names}")
        # Remaining tools after removal: ['inspect_evals/get_latest_emails', 'inspect_evals/transfer_money']
        
        return state
    return solve


@solver
def set_tool_choice(choice: Literal["forced_first", "auto", "none"]) -> Solver:
    """
    Solver that sets the tool choice to either forced_first or auto.

    Args:
        choice (Literal['forced_first', 'auto']): The choice of tool to use.
    """

    async def solve(state: TaskState, generate: Generate) -> TaskState:
        if choice == "forced_first":
            state.tool_choice = ToolFunction(name=state.metadata["target_functions"][0])
        elif choice == "auto":
            state.tool_choice = "auto"
        elif choice == "none":
            state.tool_choice = "none"
        return state

    return solve


@solver
def default_agent(
    tool_choice: Literal["forced_first", "auto", "none"] = "auto",
    user_prompt_template: str = "empty",
    system_prompt_template: Optional[str] = None,
    prompt_technique: Literal["standard", "cot", "react", "refusal"] = "standard",
) -> Solver:
    """
    Get the default solver for the harmful tools task.

    Args:
        tool_choice (Literal['forced_first', 'auto', 'none']): The choice of tool to use.
        user_prompt_template (str): Name of user prompt in `prompts.py`.
        system_prompt_template (str): Name of system prompt in `prompts.py`.
        prompt_technique (Literal['standard', 'cot', 'react', 'refusal']): Prompting technique to apply to the system prompt.
    """
    agent_setup = [
        system_prompt_based_on_model(system_prompt_template, prompt_technique),
        prompt_template(get_jailbreak_template(user_prompt_template)),
    ]

    if tool_choice in ["none", "auto"]:
        action_loop = [
            set_tool_choice(tool_choice),
            remove_one_tool(),
            generate(tool_calls="loop"),
        ]
    elif tool_choice == "forced_first":
        action_loop = [
            set_tool_choice(tool_choice),
            remove_one_tool(),
            generate(tool_calls="single"),
            set_tool_choice("auto"),
            remove_one_tool(),
            generate(tool_calls="loop"),
        ]

    plan = chain(*agent_setup, *action_loop)

    return plan
