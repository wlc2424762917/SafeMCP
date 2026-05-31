#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取JSON文件中所有的user_instruction
"""

import json
import os

def extract_user_instructions(json_file_path, output_file=None):
    """
    从JSON文件中提取所有的user_instruction
    
    Args:
        json_file_path: JSON文件路径
        output_file: 输出文件路径（可选）。如果不提供，则输出到同目录下的user_instructions.json
    """
    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    user_instructions = []
    
    # 遍历每个轨迹
    for idx, item in enumerate(data):
        instruction_data = {
            'index': idx,
            'user_instruction': None,
            'system_prompt': None
        }
        
        # 提取根层级的user_instruction
        if 'user_instruction' in item:
            instruction_data['user_instruction'] = item['user_instruction']
        
        # 提取根层级的system_prompt
        if 'system_prompt' in item:
            instruction_data['system_prompt'] = item['system_prompt']
        
        # 也可以从trajectory中提取第一个元素的user_instruction（通常与根层级相同）
        if 'trajectory' in item and len(item['trajectory']) > 0:
            first_step = item['trajectory'][0]
            if 'user_instruction' in first_step:
                instruction_data['trajectory_user_instruction'] = first_step['user_instruction']
        
        user_instructions.append(instruction_data)
    
    # 设置输出文件路径
    if output_file is None:
        output_dir = os.path.dirname(json_file_path)
        output_file = os.path.join(output_dir, 'user_instructions.json')
    
    # 保存到JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(user_instructions, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 成功提取 {len(user_instructions)} 条user_instruction")
    print(f"✓ 结果已保存到: {output_file}")
    
    # 同时保存一个纯文本版本（每行一个instruction）
    txt_file = output_file.replace('.json', '.txt')
    with open(txt_file, 'w', encoding='utf-8') as f:
        for i, item in enumerate(user_instructions):
            if item['user_instruction']:
                f.write(f"=== Instruction {i} ===\n")
                f.write(f"{item['user_instruction']}\n\n")
    
    print(f"✓ 纯文本版本已保存到: {txt_file}")
    
    return user_instructions


def extract_unique_instructions(json_file_path, output_file=None):
    """
    提取去重后的user_instruction
    
    Args:
        json_file_path: JSON文件路径
        output_file: 输出文件路径（可选）
    """
    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    unique_instructions = set()
    instruction_list = []
    
    # 遍历每个轨迹，收集唯一的instruction
    for item in data:
        if 'user_instruction' in item:
            instruction = item['user_instruction']
            if instruction and instruction not in unique_instructions:
                unique_instructions.add(instruction)
                instruction_list.append(instruction)
    
    # 设置输出文件路径
    if output_file is None:
        output_dir = os.path.dirname(json_file_path)
        output_file = os.path.join(output_dir, 'unique_user_instructions.txt')
    
    # 保存到文本文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, instruction in enumerate(instruction_list):
            f.write(f"=== Unique Instruction {i+1} ===\n")
            f.write(f"{instruction}\n\n")
    
    print(f"✓ 成功提取 {len(instruction_list)} 条唯一的user_instruction")
    print(f"✓ 结果已保存到: {output_file}")
    
    return instruction_list


if __name__ == '__main__':
    # JSON文件路径
    json_file = 'multi_step_trajectories_PS_SYSTEM_PROMPT_gpt4o-mini_final_with_metric_gemini-3-pro_ps_with_workflows_all_with_metric_4o_ps_with_workflows.json'
    
    print("=" * 60)
    print("提取所有user_instruction（包含重复）")
    print("=" * 60)
    all_instructions = extract_user_instructions(json_file)
    
    print("\n" + "=" * 60)
    print("提取唯一的user_instruction（去重）")
    print("=" * 60)
    unique_instructions = extract_unique_instructions(json_file)
    
    print("\n" + "=" * 60)
    print("统计信息")
    print("=" * 60)
    print(f"总共轨迹数: {len(all_instructions)}")
    print(f"唯一instruction数: {len(unique_instructions)}")
