import json
import os

import anthropic

MODEL = "claude-haiku-4-5-20251001"
prompt_file = "system_prompt.txt"
schema_file = "recipe_schema.json"


def generate_recipes(ingredients):
    with open(prompt_file, "r", encoding="utf-8") as f:
        system_prompt = f.read().strip()

    with open(schema_file, "r", encoding="utf-8") as f:
        schema = json.load(f)

    input_schema = {
        "type": schema["type"],
        "required": schema["required"],
        "additionalProperties": schema.get("additionalProperties", False),
        "properties": schema["properties"],
    }

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=system_prompt,
        messages=[
            {"role": "user", "content": json.dumps(ingredients, default=str)}
        ],
        tools=[{
            "name": "suggest_recipes",
            "description": "Return exactly 3 recipe suggestions based on the pantry ingredients.",
            "input_schema": input_schema,
        }],
        tool_choice={"type": "tool", "name": "suggest_recipes"},
    )

    tool_use = next(b for b in response.content if b.type == "tool_use")
    return tool_use.input["recipes"]
