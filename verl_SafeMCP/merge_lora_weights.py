#!/usr/bin/env python3
"""
Merge LoRA adapter weights into the base model for verl compatibility.

Usage:
    python merge_lora_weights.py \
        --base_model_path /path/to/huggingface \
        --output_path /path/to/merged_model

Or merge in place (will create backup):
    python merge_lora_weights.py \
        --base_model_path /path/to/huggingface \
        --merge_in_place
"""

import argparse
import os
import shutil
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel


def merge_lora_weights(base_model_path: str, output_path: str = None, merge_in_place: bool = False):
    """
    Merge LoRA adapter weights into the base model.
    
    Args:
        base_model_path: Path to the base model directory (containing lora_adapter/ subdirectory)
        output_path: Path to save the merged model. If None and merge_in_place is True, 
                     will replace the original model.
        merge_in_place: If True, merge and replace the original model (creates backup first)
    """
    base_model_path = Path(base_model_path)
    lora_adapter_path = base_model_path / "lora_adapter"
    
    # Check if lora_adapter exists
    if not lora_adapter_path.exists():
        print(f"No lora_adapter directory found at {lora_adapter_path}")
        print("The model may already be merged or doesn't have LoRA weights.")
        return
    
    print(f"Loading base model from: {base_model_path}")
    print(f"LoRA adapter path: {lora_adapter_path}")
    
    # Load the base model (use CPU first to avoid distributed init issues)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype=torch.bfloat16,
        device_map="cpu",  # Load to CPU first to avoid torch.distributed issues
        trust_remote_code=True,
        low_cpu_mem_usage=True,
    )
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
    
    print("Loading LoRA adapter...")
    # Load the LoRA adapter
    model_with_lora = PeftModel.from_pretrained(
        base_model,
        lora_adapter_path,
        torch_dtype=torch.bfloat16,
    )
    
    print("Merging LoRA weights into base model...")
    # Merge LoRA weights into the base model
    merged_model = model_with_lora.merge_and_unload()
    
    # Determine output path
    if merge_in_place:
        # Create backup
        backup_path = str(base_model_path) + "_backup_before_merge"
        if not os.path.exists(backup_path):
            print(f"Creating backup at: {backup_path}")
            shutil.copytree(base_model_path, backup_path)
        output_path = base_model_path
    elif output_path is None:
        output_path = str(base_model_path) + "_merged"
    
    print(f"Saving merged model to: {output_path}")
    
    # Save the merged model
    merged_model.save_pretrained(output_path, safe_serialization=True)
    tokenizer.save_pretrained(output_path)
    
    # Copy other necessary files that might not be saved by save_pretrained
    for filename in ["generation_config.json", "special_tokens_map.json"]:
        src_file = base_model_path / filename
        if src_file.exists() and str(output_path) != str(base_model_path):
            dst_file = Path(output_path) / filename
            if not dst_file.exists():
                shutil.copy(src_file, dst_file)
    
    # Remove lora_adapter directory from output if merging in place
    if merge_in_place:
        lora_dir_in_output = Path(output_path) / "lora_adapter"
        if lora_dir_in_output.exists():
            print(f"Removing lora_adapter directory from merged model...")
            shutil.rmtree(lora_dir_in_output)
    
    print("=" * 60)
    print("LoRA weights merged successfully!")
    print(f"   Merged model saved to: {output_path}")
    if merge_in_place:
        print(f"   Original backup at: {backup_path}")
    print("=" * 60)
    print("\nYou can now use this merged model path in your verl training script.")
    

def main():
    parser = argparse.ArgumentParser(description="Merge LoRA adapter weights into base model")
    parser.add_argument(
        "--base_model_path",
        type=str,
        required=True,
        help="Path to the base model directory containing lora_adapter/ subdirectory"
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default=None,
        help="Path to save the merged model. If not specified, will append '_merged' to base_model_path"
    )
    parser.add_argument(
        "--merge_in_place",
        action="store_true",
        help="If set, merge and replace the original model (creates backup first)"
    )
    
    args = parser.parse_args()
    
    merge_lora_weights(
        base_model_path=args.base_model_path,
        output_path=args.output_path,
        merge_in_place=args.merge_in_place,
    )


if __name__ == "__main__":
    main()

"""
    python merge_lora_weights.py \
        --base_model_path  \
        --output_path  \
"""