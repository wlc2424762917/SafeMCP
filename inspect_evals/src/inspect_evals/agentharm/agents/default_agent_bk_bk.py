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
from inspect_evals.agentharm.agents.mcp_defense_solver import mcp_defense_filter


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
def remove_filtered_tools() -> Solver:
    """Remove tools based on MCP defense filtered_tools from metadata."""
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        filtered_tools = state.metadata.get("mcp_filtered_tools", [])
        
        if not filtered_tools or not state.tools:
            return state
        
        original_count = len(state.tools)
        tool_names_before = [registry_info(tool).name.split('/')[-1] for tool in state.tools]
        
        # Remove filtered tools
        state.tools = [
            tool for tool in state.tools
            if registry_info(tool).name.split('/')[-1] not in filtered_tools
        ]
        
        removed_count = original_count - len(state.tools)
        if removed_count > 0:
            tool_names_after = [registry_info(tool).name.split('/')[-1] for tool in state.tools]
            print(f"\033[92m[Tool Removal] Removed {removed_count} tools: {set(tool_names_before) - set(tool_names_after)}\033[0m")
            print(f"\033[92m[Tool Removal] Remaining tools: {tool_names_after}\033[0m")
        
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
    use_mcp_defense: bool = False,
) -> Solver:
    """
    Get the default solver for the harmful tools task.

    Args:
        tool_choice (Literal['forced_first', 'auto', 'none']): The choice of tool to use.
        user_prompt_template (str): Name of user prompt in `prompts.py`.
        system_prompt_template (str): Name of system prompt in `prompts.py`.
        prompt_technique (Literal['standard', 'cot', 'react', 'refusal']): Prompting technique to apply to the system prompt.
        use_mcp_defense (bool): Whether to use MCP defense for tool filtering.
    """
    agent_setup = [
        system_prompt_based_on_model(system_prompt_template, prompt_technique),
        prompt_template(get_jailbreak_template(user_prompt_template)),
        # pre-filter tools based on user instruction
        mcp_defense_filter(enable=use_mcp_defense, initial_filter=True),
        remove_filtered_tools(),
    ]

    if tool_choice in ["none", "auto"]:
        action_loop = [
            set_tool_choice(tool_choice),
            generate(tool_calls="loop"),
            mcp_defense_filter(enable=use_mcp_defense),
            remove_filtered_tools(),
        ]
    elif tool_choice == "forced_first":
        action_loop = [
            set_tool_choice(tool_choice),
            generate(tool_calls="single"),
            mcp_defense_filter(enable=use_mcp_defense),
            remove_filtered_tools(),
            set_tool_choice("auto"),
            generate(tool_calls="loop"),
            mcp_defense_filter(enable=use_mcp_defense),
            remove_filtered_tools(),
        ]

    plan = chain(*agent_setup, *action_loop)

    return plan
