from transformers import AutoTokenizer, AutoModelForCausalLM
from pathlib import Path

src = "/share/project/shared/models/qwen/Qwen3-4B-Instruct-2507"
dst = "/etc/tmp_model/Qwen3-4B-Instruct-2507-with-safety-tools"
Path(dst).mkdir(parents=True, exist_ok=True)


tokenizer = AutoTokenizer.from_pretrained(src, use_fast=True, trust_remote_code=True)
sp_safety = tokenizer.encode("<|safety|>", add_special_tokens=False)

import ipdb; ipdb.set_trace()