import sys; import os; sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .structure_validator import validate_action_plan
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json
load_dotenv() 


def _print_debug_json(label, payload):
    print(f"{label}:")
    print(json.dumps(payload, ensure_ascii=True, indent=2))


def gemini_init():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment")
    return genai.Client(api_key=api_key)

def provider_gemini(system_prompt, user_prompt, model_name):
    client = gemini_init()
    res = client.models.generate_content(
        model=model_name,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
        ),
    )

    response_text = (res.text or "").strip()
    valid, data_or_error = validate_action_plan(response_text)
    if valid:
        _print_debug_json("Validated JSON response", data_or_error)
        return data_or_error

    print(f"Gemini response validation failed: {data_or_error}")
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

 
