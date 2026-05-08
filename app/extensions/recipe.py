import json

import requests

api_url = "http://localhost:1234/v1"
model = ""
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

def generate_recipes(ingredients):
    with open(prompt_file, "r", encoding="utf-8") as f:
        system_prompt = f.read().strip()

    with open(schema_file, "r", encoding="utf-8") as f:
        recipe_schema = json.load(f)

    response = requests.post(
        f"{api_url}/chat/completions",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(ingredients, default=str)},
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "RecipeSuggestions",
                    "schema": recipe_schema,
                    "strict": True,
                },
            },
            **parameters,
        },
    )
    response.raise_for_status()

    message = response.json()["choices"][0]["message"]
    content = message.get("content") or message.get("reasoning_content", "")
    print("LM Studio response content:", repr(content[:200]))
    return json.loads(content)["recipes"]
