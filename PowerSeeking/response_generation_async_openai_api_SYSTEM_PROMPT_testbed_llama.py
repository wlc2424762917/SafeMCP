import os
import time
import json
import random
import asyncio
import logging
from typing import List, Dict, Any, Optional
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from synthetic_tools import AVAILABLE_TOOLS
from tqdm.asyncio import tqdm_asyncio

# Configuration
MODEL_PATH = "./Llama-3.1-8B-Instruct"
MODEL_NAME = "Llama-3.1-8B-Instruct"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

def fix_tool_schemas(tools: list) -> list:
    """
    Fix tool schemas by adding missing 'items' field to array types.
    """
    def fix_schema_recursive(schema):
        if isinstance(schema, dict):
            if schema.get('type') == 'array' and 'items' not in schema:
                schema['items'] = {'type': 'string'}
            for key, value in schema.items():
                if isinstance(value, dict):
                    fix_schema_recursive(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            fix_schema_recursive(item)
        return schema
    
    fixed_tools = []
    for tool in tools:
        tool_copy = json.loads(json.dumps(tool))
        if 'function' in tool_copy and 'parameters' in tool_copy['function']:
            fix_schema_recursive(tool_copy['function']['parameters'])
        fixed_tools.append(tool_copy)
    return fixed_tools


class LlamaClient:
    _instance = None
    _model = None
    _tokenizer = None

    @classmethod
    def get_client(cls, model_path: str = MODEL_PATH):
        if cls._model is None:
            logger.info(f"Loading model from {model_path}...")
            cls._tokenizer = AutoTokenizer.from_pretrained(model_path)
            cls._model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.bfloat16,
                device_map="auto",
                trust_remote_code=True
            )
            logger.info("Model loaded successfully!")
        return cls._model, cls._tokenizer


def convert_tools_to_llama_format(tools: list) -> list:
    """
    Convert OpenAI-style tools to Llama-compatible format.
    Llama expects tools with 'name', 'description', and 'parameters'.
    """
    llama_tools = []
    for tool in tools:
        if 'function' in tool:
            func = tool['function']
            llama_tools.append({
                "type": "function",
                "function": {
                    "name": func.get('name', ''),
                    "description": func.get('description', ''),
                    "parameters": func.get('parameters', {})
                }
            })
        else:
            # Already in correct format
            llama_tools.append(tool)
    return llama_tools


def parse_tool_calls_from_text(response_text: str) -> Optional[List[Dict]]:
    """
    Parse tool calls from model response text.
    Handles multiple formats for robustness.
    """
    try:
        import re
        
        # Look for ```json blocks first
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
            data = json.loads(json_str)
            if 'tool_calls' in data:
                return data['tool_calls']
            # Handle single tool call in JSON block
            if 'name' in data:
                return [data]
        
        # Try to find raw JSON with tool_calls
        json_match = re.search(r'\{[^{}]*"tool_calls"[^{}]*\[.*?\]\s*\}', response_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            if 'tool_calls' in data:
                return data['tool_calls']
        
        # Try to parse the entire response as JSON - could be a direct tool call
        response_stripped = response_text.strip()
        if response_stripped.startswith('{') and response_stripped.endswith('}'):
            data = json.loads(response_stripped)
            if 'tool_calls' in data:
                return data['tool_calls']
            # Handle direct tool call format: {"name": "...", "parameters": {...}}
            if 'name' in data:
                return [data]
        
        # Try to find tool call pattern like {"name": "tool_name", "parameters": {...}}
        # This handles cases where the model outputs tool calls directly
        tool_pattern = r'\{[^{}]*"name"\s*:\s*"[^"]+"\s*,\s*"(?:parameters|arguments)"\s*:\s*\{[^}]*\}\s*\}'
        matches = re.findall(tool_pattern, response_text, re.DOTALL)
        if matches:
            tool_calls = []
            for match in matches:
                try:
                    tool_data = json.loads(match)
                    # Normalize to use "arguments" key
                    if 'parameters' in tool_data and 'arguments' not in tool_data:
                        tool_data['arguments'] = tool_data.pop('parameters')
                    tool_calls.append(tool_data)
                except json.JSONDecodeError:
                    continue
            if tool_calls:
                return tool_calls
            
    except (json.JSONDecodeError, AttributeError) as e:
        logger.debug(f"Failed to parse tool calls: {e}")
        pass
    
    return None


def generate_response(model, tokenizer, messages: list, tools: Optional[list] = None, max_new_tokens: int = 2048) -> str:
    """
    Generate a response using the Llama model with optional tool support.
    
    Args:
        model: The loaded Llama model
        tokenizer: The tokenizer for the model
        messages: List of conversation messages
        tools: Optional list of tools available to the model
        max_new_tokens: Maximum number of tokens to generate
    
    Returns:
        Generated response text
    """
    # Apply chat template with tools support
    try:
        if tools:
            # Try using native tools support in Llama 3.1+
            text = tokenizer.apply_chat_template(
                messages,
                tools=tools,
                tokenize=False,
                add_generation_prompt=True
            )
        else:
            text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
    except Exception as e:
        # Fallback if tools parameter is not supported
        logger.warning(f"Native tools support failed, using fallback: {e}")
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
    
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode only the new tokens
    response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    return response.strip()


async def process_chat_loop(messages: list, tools: list, function_map: dict) -> list:
    """
    Process chat loop with tool calls using Llama's native tool support.
    
    Args:
        messages: List of conversation messages
        tools: List of available tools
        function_map: Dictionary mapping tool names to callable functions
    
    Returns:
        List of all messages including tool calls and responses
    """
    model, tokenizer = LlamaClient.get_client()
    sequential_responses = messages.copy()
    
    # Convert tools to Llama format
    llama_tools = convert_tools_to_llama_format(tools)
    
    # Start with the initial messages
    conversation_history = messages.copy()
    
    try:
        # Run in executor to not block event loop
        loop = asyncio.get_event_loop()
        
        # Generate initial response with tools
        response_text = await loop.run_in_executor(
            None, 
            lambda: generate_response(model, tokenizer, conversation_history, llama_tools)
        )
        
        # Check for tool calls
        tool_calls = parse_tool_calls_from_text(response_text)
        
        # Create response dict
        message_dict = {
            "role": "assistant",
            "content": response_text
        }
        
        # Use a call counter for unique IDs
        call_counter = 0

        if tool_calls:
            logger.info(f"Initial response contains {len(tool_calls)} tool call(s)")
            message_dict["tool_calls"] = [
                {
                    "id": f"call_{call_counter + i}",
                    "type": "function",
                    "function": {
                        "name": tc.get("name", tc.get("function", {}).get("name", "")),
                        "arguments": json.dumps(tc.get("arguments", tc.get("parameters", {}))) if isinstance(tc.get("arguments", tc.get("parameters", {})), dict) else tc.get("arguments", tc.get("parameters", "{}"))
                    }
                }
                for i, tc in enumerate(tool_calls)
            ]
            call_counter += len(tool_calls)
        else:
            logger.info("No tool calls detected in initial response")

        # Add to both histories
        conversation_history.append(message_dict)
        sequential_responses.append(message_dict)
        
        # Handle tool calls loop
        max_iterations = 10
        iteration = 0
        has_executed_tools = False  # Track if we've executed any tools
        
        while tool_calls and iteration < max_iterations:
            iteration += 1
            has_executed_tools = True
            logger.info(f"Tool call iteration {iteration}/{max_iterations}, processing {len(tool_calls)} tool(s)")
            
            # Get the tool call IDs from the last assistant message
            last_assistant_msg = sequential_responses[-1]
            tool_call_ids = [tc["id"] for tc in last_assistant_msg.get("tool_calls", [])]
            
            # Process each tool call
            for i, tc in enumerate(tool_calls):
                function_name = tc.get("name", tc.get("function", {}).get("name", ""))
                function_params = tc.get("arguments", tc.get("parameters", {}))
                
                # Normalize arguments to dict
                if isinstance(function_params, str):
                    try:
                        function_params = json.loads(function_params)
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse arguments: {function_params}")
                        function_params = {}
                
                # Execute the tool
                try:
                    if function_name in function_map:
                        function_result = function_map[function_name](**function_params)
                        function_result_str = json.dumps(function_result, ensure_ascii=False)
                        logger.info(f"Executed tool: {function_name}")
                    else:
                        function_result_str = json.dumps({"error": f"Tool {function_name} not found"})
                        logger.error(f"Tool not found: {function_name}")
                except Exception as e:
                    error_msg = f"Tool execution error: {str(e)}"
                    logger.error(error_msg)
                    function_result_str = json.dumps({"error": error_msg})
                
                # Create tool response message with matching ID
                tool_call_id = tool_call_ids[i] if i < len(tool_call_ids) else f"call_{call_counter - len(tool_calls) + i}"
                tool_response = {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "name": function_name,
                    "content": function_result_str
                }
                
                # Add tool result to both histories
                conversation_history.append(tool_response)
                sequential_responses.append(tool_response)
            
            # Generate next response with tools
            response_text = await loop.run_in_executor(
                None,
                lambda: generate_response(model, tokenizer, conversation_history, llama_tools)
            )
            
            # Check for more tool calls
            tool_calls = parse_tool_calls_from_text(response_text)
            
            message_dict = {
                "role": "assistant",
                "content": response_text
            }

            if tool_calls:
                logger.info(f"Found {len(tool_calls)} more tool call(s) in response")
                message_dict["tool_calls"] = [
                    {
                        "id": f"call_{call_counter + i}",
                        "type": "function",
                        "function": {
                            "name": tc.get("name", tc.get("function", {}).get("name", "")),
                            "arguments": json.dumps(tc.get("arguments", tc.get("parameters", {}))) if isinstance(tc.get("arguments", tc.get("parameters", {})), dict) else tc.get("arguments", tc.get("parameters", "{}"))
                        }
                    }
                    for i, tc in enumerate(tool_calls)
                ]
                call_counter += len(tool_calls)
            else:
                logger.info("No more tool calls detected, finishing loop")
            
            # Add to both histories
            conversation_history.append(message_dict)
            sequential_responses.append(message_dict)
        
        if iteration >= max_iterations:
            logger.warning(f"Reached maximum iterations ({max_iterations})")
        
        # If tools were executed but no final response without tool calls, generate one
        if has_executed_tools and tool_calls:
            logger.info("Generating final response after tool execution")
            # Add a prompt to generate final answer
            conversation_history.append({
                "role": "user",
                "content": "Based on the tool results above, please provide your final response."
            })
            sequential_responses.append({
                "role": "user", 
                "content": "Based on the tool results above, please provide your final response."
            })
            
            final_response_text = await loop.run_in_executor(
                None,
                lambda: generate_response(model, tokenizer, conversation_history, llama_tools)
            )
            
            final_message_dict = {
                "role": "assistant",
                "content": final_response_text
            }
            conversation_history.append(final_message_dict)
            sequential_responses.append(final_message_dict)
        
        return sequential_responses
        
    except Exception as e:
        error_msg = f"Error in chat processing: {str(e)}"
        logger.error(error_msg)
        import traceback
        logger.error(traceback.format_exc())
        return sequential_responses if sequential_responses else [{"role": "assistant", "content": error_msg}]


async def process_instruction_batch(batch: list, sem: asyncio.Semaphore) -> list:
    batch_results = []
    
    async def process_single_group(group_data):
        """
        Process a single group of scenarios.
        """
        async with sem:
            results = []
            tools_config = group_data.get("tools", [])
            tools_config = json.loads(tools_config)
            
            # Fix tool schemas
            tools = fix_tool_schemas(tools_config)

            # Extract System Prompt and User Instruction
            toxic_system_prompt = group_data.get("system_prompt", "")
            benign_user_instruction = group_data.get("user_instruction", "")
            
            if not toxic_system_prompt or not benign_user_instruction:
                return []

            # Construct Messages
            messages = [
                {"role": "system", "content": toxic_system_prompt},
                {"role": "user", "content": benign_user_instruction}
            ]
            print("toxic_system_prompt: ", toxic_system_prompt)
            # Run the Agent Loop
            chat_history = await process_chat_loop(
                messages,
                tools,
                AVAILABLE_TOOLS
            )
            
            # Store Result
            results.append({
                "pattern": group_data.get("pattern"),
                "system_prompt": toxic_system_prompt,
                "user_instruction": benign_user_instruction,
                "chat_history": chat_history,
                "model_name": MODEL_NAME
            })
            
            return results
    
    tasks = [process_single_group(item) for item in batch]
    nested_results = await asyncio.gather(*tasks)
    
    # Flatten list of lists
    for res_list in nested_results:
        if res_list:
            batch_results.extend(res_list)
            
    return batch_results


async def get_multi_step_response_async(
    instruction_groups: list,
    output_file: str,
    batch_size: int = 1,  # Process 1 at a time for local model
    recover: bool = False
) -> list:
    all_responses = []
    
    sem = asyncio.Semaphore(batch_size)
    
    # Batch the groups
    batches = [instruction_groups[i:i + batch_size] for i in range(0, len(instruction_groups), batch_size)]

    for batch_idx, batch in enumerate(tqdm_asyncio(batches)):
        logger.info(f"Processing batch {batch_idx + 1}/{len(batches)}")
        batch_results = await process_instruction_batch(batch, sem)
        all_responses.extend(batch_results)
        
        # Save periodically
        if batch_idx % 2 == 0:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(all_responses, f, indent=4, ensure_ascii=False)
    
    # Final Save
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_responses, f, indent=4, ensure_ascii=False)
    
    return all_responses


if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.abspath(__file__))

    input_file_path = "./multi_step_trajectory_generation/trajectories/multi_step_trajectories_PS_SYSTEM_PROMPT_gpt4o-mini_final_with_metric_gemini-3-pro_ps_with_workflows_all.json"

    if not os.path.exists(input_file_path):
        logger.error(f"Input file not found: {input_file_path}")
        exit(1)

    with open(input_file_path, "r", encoding="utf-8") as f:
        instruction_groups = json.load(f)
    
    # Output File
    output_file_path = os.path.join(
        cur_dir, 
        "testbed_trajectories",
        f"multi_step_trajectories_PowerSeeking_{MODEL_NAME}_testbed.json"
    )
    
    # Ensure output dir exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Pre-load the model
    logger.info("Pre-loading Llama model...")
    LlamaClient.get_client()

    asyncio.run(
        get_multi_step_response_async(
            instruction_groups,
            output_file_path,
            batch_size=1,  # Use batch_size=1 for local model to avoid OOM
            recover=True
        )
    )
