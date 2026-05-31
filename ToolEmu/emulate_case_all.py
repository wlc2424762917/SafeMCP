import os
import json
from argparse import Namespace
from functools import partial
from toolemu.agents.agent_executor import AgentExecutorWithToolkit
import tiktoken
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from dotenv import load_dotenv

load_dotenv()
from toolemu.agent_executor_builder import build_agent_executor
from toolemu.utils import (
    construct_trajec,
    construct_simple_trajec,
    append_file,
    get_fixed_model_name,
    load_openai_llm,
    get_toolkit_names,
    case_to_input_dict,
    read_file,
    make_colorful,
    print_prompt,
)
import torch

show_prompt = False

# agent_llm_name = "gpt-4"
agent_llm_name = "gpt-4o"  # base model for the agent, choose from ["gpt-4", "gpt-3.5-turbo-16k", "claude-2"]
agent_temp = 0.0  # agent temperature
simulator_llm = "gpt-4o"  # base model for the emulator, we fix it to gpt-4 for the best emulation performance
simulator_type = "adv_thought"  # emulator type, choose from ["std_thought", "adv_thought"] for standrd or adversarial emulation



agent_llm = load_openai_llm(
    model_name=get_fixed_model_name(agent_llm_name),
    temperature=agent_temp,
    request_timeout=300,
    callbacks=[StreamingStdOutCallbackHandler()],
)

# The emulator LLM
simulator_llm = load_openai_llm(
    model_name=get_fixed_model_name(simulator_llm),
    temperature=0.0,
    request_timeout=300,
    callbacks=[StreamingStdOutCallbackHandler()],
)

mcp_defense_tok, mcp_defense_model = load_openai_llm(
    model_name="mcp_defense_qwen",
    temperature=0.0,
    callbacks=[StreamingStdOutCallbackHandler()],
)

mcp_defense_model.to("cuda")
mcp_defense_tok.to("cuda")

build_agent_executor = partial[type[AgentExecutorWithToolkit]](
    build_agent_executor,
    agent_llm=agent_llm,
    simulator_llm=simulator_llm,
)


def query_agent(case, simulator_type="std_thought", max_iterations=15):
    agent_executor = build_agent_executor(
        get_toolkit_names(case),
        simulator_type=simulator_type,
        mcp_defense_tok=mcp_defense_tok,
        mcp_defense_model=mcp_defense_model,
    )
    prompt_inputs = case_to_input_dict(case)

    if "adv" in simulator_type:
        output = agent_executor(prompt_inputs)
    else:
        output = agent_executor(prompt_inputs["input"])
    
    return output, agent_executor


def display_prompt(prompt):
    print(make_colorful("human", prompt.split("Human:")[1]))

cases = read_file("./assets/all_cases.json")

from toolemu.utils import append_jsonl, replace_agent_action_with_list


def save_traj(path, results):
    # This is an ad-hoc fix for dumping langchain result
    results = replace_agent_action_with_list(results)
    sim_type = "Standard" if simulator_type == "std_thought" else "Adversarial"
    results["sim_type"] = sim_type
    results["agent_llm"] = agent_llm_name
    results["agent_temp"] = agent_temp
    results["case_idx"] = case_idx
    results["case"] = case

    append_jsonl(path, results)


case_idx = 0
max_idx = 144

retry_count = {}
max_retries = 3  # Max request retries
while case_idx < max_idx:
    print("simulating: ", case_idx)
    case = cases[case_idx]

    agent_executor = build_agent_executor(
        toolkits=get_toolkit_names(case),
        simulator_type=simulator_type,
    )
    
    agent_prompt_temp = agent_executor.agent.llm_chain.prompt
    agent_prompt = agent_prompt_temp.format(
        **{k: "test" for k in agent_prompt_temp.input_variables}
    )
    if show_prompt:
        display_prompt(agent_prompt)


    simulator_prompt_temp = agent_executor.llm_simulator_chain.prompt
    simulator_prompt = simulator_prompt_temp.format(
        **{k: "test" for k in simulator_prompt_temp.input_variables}
    )
    if show_prompt:
        display_prompt(simulator_prompt)
        print("\n\n>>>>Token lengths:", len(encoding.encode(simulator_prompt)))

    try:
        results, executor = query_agent(case=case, simulator_type=simulator_type)
    except Exception as e:
        print(f"query_agent failed for case_idx={case_idx}, error: {e}")
        retry_count[case_idx] = retry_count.get(case_idx, 0) + 1
        if retry_count[case_idx] >= max_retries:
            print(f"case_idx={case_idx} failed {max_retries} times, skipping...")
            case_idx += 1
        else:
            print(f"Retrying case_idx={case_idx} (attempt {retry_count[case_idx] + 1}/{max_retries})")
        continue

    simplified_traj = construct_simple_trajec(results)
    print(simplified_traj)
    
    save_file_path = f"./dumps/notebook/res.jsonl"

    print(f"saving to {save_file_path}")
    try:
        save_traj(save_file_path, results)
        case_idx += 1
    except Exception as e:
        print(f"Save failed for case_idx={case_idx}, error: {e}")
        retry_count[case_idx] = retry_count.get(case_idx, 0) + 1
        if retry_count[case_idx] > 2:
            print(f"case_idx={case_idx} failed too many times, skip.")
            case_idx += 1
        else:
            print(f"Retrying case_idx={case_idx} by re-emulating")
            case_idx = max(0, case_idx)
        continue