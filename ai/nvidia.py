from .structure_validator import validate_action_plan
from dotenv import load_dotenv
import os
import json
from openai import OpenAI  # NVIDIA NIM is OpenAI-compatible

load_dotenv()

def _print_debug_json(label, payload):
    print(f"{label}:")
    print(json.dumps(payload, ensure_ascii=True, indent=2))


def nvidia_init():
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY not found in environment")
    
    # NVIDIA NIM / OpenAI-compatible client
    return OpenAI(
        api_key=api_key,
        base_url="https://integrate.api.nvidia.com/v1"  # change if needed
    )


def provider_nvidia(system_prompt, user_prompt, model_name):
    client = nvidia_init()

    res = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
    )

    response_text = (res.choices[0].message.content or "").strip()

    valid, data_or_error = validate_action_plan(response_text)
    if valid:
        _print_debug_json("Validated JSON response", data_or_error)
        return data_or_error

    print(f"NVIDIA response validation failed: {data_or_error}")

    if response_text:
        normalized = response_text.strip()
        if normalized in {"{}", "[]", "null"}:
            normalized = "I could not understand the request format. Please try rephrasing your request."

        fallback_response = {
            "type": "text",
            "tool": None,
            "args": None,
            "response": normalized,
        }

        _print_debug_json("Normalized fallback JSON response", fallback_response)
        return fallback_response

    return None