import os
import time
import json
import random
import asyncio
import logging
from openai import AsyncOpenAI
from synthetic_tools import AVAILABLE_TOOLS
from tqdm.asyncio import tqdm_asyncio

# Configuration
API_KEY = ""
BASE_URL = ''
MODEL = "gpt-4o-mini"
# MODEL = "gemini-2.5-flash"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Default system prompt is NO LONGER USED globally.
# We will use the specific 'system_prompt' from each scenario.

def fix_tool_schemas(tools: list) -> list:
    """
    Fix tool schemas by adding missing 'items' field to array types.
    OpenAI API requires all array parameters to have an 'items' field.
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

class OpenAIClient:
    _instance = None
    _client = None

    @classmethod
    def get_client(cls, api_key: str = API_KEY, base_url: str = BASE_URL) -> AsyncOpenAI:
        if cls._client is None:
            cls._client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        return cls._client

async def async_retry(func, max_retries=10, delay=5):
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Max retries reached. Error: {str(e)}")
                raise
            logger.warning(f"Attempt {attempt + 1} failed. Error: {str(e)}. Retrying in {delay}s...")
            await asyncio.sleep(delay)

async def create_chat_completion(client, messages: list, tools: list):
    return await client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools
    )

async def process_chat_loop(messages: list, tools: list, function_map: dict) -> list:
    client = OpenAIClient.get_client()
    sequential_responses = messages.copy()
    
    try:
        async def make_request():
            return await create_chat_completion(client, messages, tools)
        
        # Initial Request
        response = await async_retry(make_request)
        
        # Append Assistant Response
        message_dict = {
            "role": response.choices[0].message.role,
            "content": response.choices[0].message.content
        }
        if response.choices[0].message.tool_calls:
            message_dict["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in response.choices[0].message.tool_calls
            ]
        
        messages.append(message_dict)
        sequential_responses.append(response.model_dump())
        
        # Handle Tool Calls Loop
        while response.choices[0].finish_reason == "tool_calls":
            for tool_call in response.choices[0].message.tool_calls:
                function_name = tool_call.function.name
                function_params = json.loads(tool_call.function.arguments)
                
                try:
                    # Execute the tool using the synthetic_tools map
                    if function_name in function_map:
                        function_result = json.dumps(
                            function_map[function_name](**function_params),
                            ensure_ascii=False
                        )
                    else:
                        function_result = json.dumps({"error": f"Tool {function_name} not found"})
                except Exception as e:
                    error_msg = f"Tool execution error: {str(e)}"
                    logger.error(error_msg)
                    function_result = json.dumps({"error": error_msg})
                
                tool_response = {
                    "role": "tool",
                    "name": function_name,
                    "content": function_result,
                    "tool_call_id": tool_call.id
                }
                messages.append(tool_response)
                sequential_responses.append(tool_response)
            
            # Get next response from model
            try:
                response = await async_retry(make_request)
                
                message_dict = {
                    "role": response.choices[0].message.role,
                    "content": response.choices[0].message.content
                }
                if response.choices[0].message.tool_calls:
                    message_dict["tool_calls"] = [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in response.choices[0].message.tool_calls
                    ]
                
                messages.append(message_dict)
                sequential_responses.append(response.model_dump())
            except Exception as e:
                error_msg = f"Error in chat processing: {str(e)}"
                logger.error(error_msg)
                return error_msg
        
        return sequential_responses
    except Exception as e:
        error_msg = f"Error in chat processing: {str(e)}"
        logger.error(error_msg)
        return error_msg

async def process_instruction_batch(batch: list, sem: asyncio.Semaphore) -> list:
    batch_results = []
    
    async def process_single_group(group_data):
        """
        Process a single group of scenarios (from one generation prompt).
        Each 'group_data' contains a 'scenarios' list with 5 items.
        """
        async with sem:

            results = []
            tools_config = group_data.get("tools", [])
            tools_config = json.loads(tools_config)
            # import ipdb; ipdb.set_trace()
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
            
            # Run the Agent Loop
            chat_history = await process_chat_loop(
                messages,
                tools,
                AVAILABLE_TOOLS
            )
            
            # Store Result
            results.append({
                # "category": group_data.get("category"),
                # "sub_category": group_data.get("sub_category"),
                "pattern": group_data.get("pattern"),
                "system_prompt": toxic_system_prompt,
                "user_instruction": benign_user_instruction,
                # "environment_setup": group_data.get("environment_setup"),
                # "expected_trajectory": group_data.get("expected_trajectory"),
                "chat_history": chat_history,
                "model_name": MODEL
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
    batch_size: int = 5, # Process 5 groups (25 scenarios) concurrently
    recover: bool = False
) -> list:
    all_responses = []
    
    sem = asyncio.Semaphore(batch_size)
    
    # Batch the groups
    batches = [instruction_groups[i:i + batch_size] for i in range(0, len(instruction_groups), batch_size)]
    
    # import ipdb; ipdb.set_trace()

    for batch_idx, batch in enumerate(tqdm_asyncio(batches)):
        # if batch_idx <= 62:
        #     continue
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
    

    
    
    
    

    input_file_path = "trajectories/multi_step_trajectories_PS_SYSTEM_PROMPT_gpt4o-mini_final_with_metric_gemini-3-pro_ps_with_workflows_all.json"

    if not os.path.exists(input_file_path):
        logger.error(f"Input file not found: {input_file_path}")
        exit(1)

    with open(input_file_path, "r", encoding="utf-8") as f:
        instruction_groups = json.load(f)
    
    import ipdb; ipdb.set_trace()
    # Output File
    output_file_path = os.path.join(
        cur_dir, 
        "testbed_trajectories",
        "multi_step_trajectories_PS_SYSTEM_PROMPT_agentharm_tools_gpt4o-mini_redo_redo.json"
    )
    
    # Ensure output dir exists
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    asyncio.run(
        get_multi_step_response_async(
            instruction_groups,
            output_file_path,
            batch_size=1,
            recover=True
        )
    )