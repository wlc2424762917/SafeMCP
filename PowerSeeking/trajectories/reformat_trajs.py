import json

def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    # input_path = "/data/wanglichao/AgentAlign/multi_step_trajectory_generation/multi_step_responses_gpt-4o_patch_round_1_tool_chain_harm_and_benign_instruction_benign.json"
    # output_path = "/data/wanglichao/AgentAlign/multi_step_trajectory_generation/multi_step_responses_gpt-4o_patch_round_1_tool_chain_harm_and_benign_instruction_benign_formatted.json"
   
    # input_path = "/share/project/wlc/AgentAlign_ps/multi_step_trajectory_generation/multi_step_responses_powerseeking_gpt-4o-mini_ds_r1_ps_round_0.json"
    # output_path = "/share/project/wlc/AgentAlign_ps/multi_step_trajectory_generation/multi_step_responses_powerseeking_gpt-4o-mini_ds_r1_ps_round_0_formatted.json"
    
    # input_path = "/media/lc/Data/AgentAlign_ps_all_tools/multi_step_trajectory_generation/trajectories/multi_step_trajectories_PS_SYSTEM_PROMPT_agentharm_tools_gpt4o-mini_start_2.json"
    # output_path = "/media/lc/Data/AgentAlign_ps_all_tools/multi_step_trajectory_generation/trajectories/multi_step_trajectories_PS_SYSTEM_PROMPT_agentharm_tools_gpt4o-mini_start_2_formatted.json"
    
    # input_path = "/media/lc/Data/AgentAlign_ps_all_tools/multi_step_trajectory_generation/trajectories/multi_step_trajectories_PS_SYSTEM_PROMPT_agentharm_tools_gpt4o-mini_start_2_B2.json"
    # output_path = "/media/lc/Data/AgentAlign_ps_all_tools/multi_step_trajectory_generation/trajectories/multi_step_trajectories_PS_SYSTEM_PROMPT_agentharm_tools_gpt4o-mini_start_2_B2_formatted.json"
    
    input_path = "/media/lc/Data/AgentAlign_ps_all_tools/multi_step_trajectory_generation/trajectories/multi_step_trajectories_PS_SYSTEM_PROMPT_agentharm_tools_gpt4o-mini_after_2_B3.json"
    output_path = "/media/lc/Data/AgentAlign_ps_all_tools/multi_step_trajectory_generation/trajectories/multi_step_trajectories_PS_SYSTEM_PROMPT_agentharm_tools_gpt4o-mini_after_2_B3_formatted.json"
    
    data = read_json(input_path)
    print(len(data))
    formatted_data = [] 
    
    # import ipdb; ipdb.set_trace()
    
    
    for item in data:
        # dict_keys(['pattern', 'instruction_index', 'chat_history'])
        # print(item)
        # break
        pattern = item['pattern']
        chat_history = item['chat_history']
        # print(chat_history)
        if not isinstance(chat_history, list):
            continue
        # import ipdb; ipdb.set_trace()
        system_prompt = chat_history[0]['content']
        user_instruction = chat_history[1]['content']
        traj_steps = chat_history[2:-1]
        output_message = chat_history[-1]['choices'][0]["message"]['content']
        formatted_traj_steps = [{"system_prompt": system_prompt, "user_instruction": user_instruction}]
        # import ipdb; ipdb.set_trace()
        acts = []
        obs = []
        for cur_step in traj_steps:
            if "id" in cur_step:
                content = cur_step['choices'][0]["message"]['content']
                if content != None:
                    thought = content
                else:
                    thought = ""
                tool_calls = cur_step['choices'][0]["message"]["tool_calls"] 
                thought_actions = {
                    "thought": thought,
                    "action": [],
                    "action_input": [],
                    "tool_call_ids": [],
                    "observation": []
                }
                for tool_call in tool_calls:
                    tool_name = tool_call['function']['name']
                    tool_input = tool_call['function']['arguments']
                    tool_input = json.loads(tool_input)
                    tool_call_id = tool_call['id']
                     
                    thought_actions["action"].append(tool_name)
                    thought_actions["action_input"].append(tool_input)
                    thought_actions["tool_call_ids"].append(tool_call_id)
                acts.append(thought_actions)
            elif cur_step["role"] == "tool":
                tool_name = cur_step['name']
                observation = cur_step['content']
                observation = json.loads(observation)
                tool_call_id = cur_step['tool_call_id']
                obs.append({tool_call_id: observation})

        for act in acts:
            tool_call_ids = act["tool_call_ids"]
            for tool_call_id in tool_call_ids:
                # import ipdb; ipdb.set_trace()
                for cur_obs in obs:
                    if tool_call_id in cur_obs:
                        act["observation"].append(cur_obs[tool_call_id])
                        print(f"action {act['action']} is associated with observation {cur_obs[tool_call_id]}")
                        # break
            formatted_traj_steps.append(act)
        for formatted_step in formatted_traj_steps:
            # import ipdb; ipdb.set_trace()
            if "tool_call_ids" in formatted_step:
                formatted_step.pop("tool_call_ids")
        print(formatted_traj_steps)
        formatted_traj_steps.append({"output": output_message})
        formatted_item = {
            "pattern": pattern,
            "trajectory": formatted_traj_steps
        }
        formatted_data.append(formatted_item)
        # import ipdb; ipdb.set_trace()

    with open(output_path, 'w') as f:
        json.dump(formatted_data, f, indent=4)