import json

import jsonschema
import requests

api_url = "http://localhost:1234/v1"
model = "qwen/qwen3.5-9b"
prompt_file = "system_prompt.txt"
schema_file = "recipe_schema.json"

parameters = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 20,
    "presence_penalty": 1.5,
    "max_tokens": 6144,
    "enable_thinking": False,
}