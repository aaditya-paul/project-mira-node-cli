from .structure_validator import validate_action_plan
from dotenv import load_dotenv
import os
import json
from groq import Groq

load_dotenv()

def _print_debug_json(label, payload):
    print(f"{label}:")
    print(json.dumps(payload, ensure_ascii=True, indent=2))

def _shorten_context(system_prompt, user_prompt, max_chars=10000):
    """
    Keep system prompt mostly intact, aggressively trim user prompt.
    """
    # Reserve space for system prompt (important instructions)
    sys_max = int(max_chars * 0.4)
    usr_max = int(max_chars * 0.6)

    short_system = system_prompt[:sys_max]

    if len(user_prompt) > usr_max:
        short_user = user_prompt[:usr_max] + "\n...[truncated]"
    else:
        short_user = user_prompt

    return short_system, short_user


def _build_messages(system_prompt, user_prompt):
    # Groq requires the word 'json' to appear in messages when using json_object mode.
    json_guard = "IMPORTANT: Return only a valid json object. Do not include markdown or extra text."
    return [
        {"role": "system", "content": f"{system_prompt}\n\n{json_guard}"},
        {"role": "user", "content": user_prompt},
    ]

def groq_init():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment")
    
    return Groq(api_key=api_key)

def provider_groq(system_prompt, user_prompt, model_name):
    client = groq_init()

    # 🔥 shrink context BEFORE sending
    system_prompt, user_prompt = _shorten_context(system_prompt, user_prompt)
    messages = _build_messages(system_prompt, user_prompt)

    try:
        res = client.chat.completions.create(
            model=model_name,
            messages=messages,
            response_format={"type": "json_object"},
        )
    except Exception as e:
        if "Request too large" in str(e):
            print("Context still too large, retrying with aggressive trim...")

            system_prompt, user_prompt = _shorten_context(
                system_prompt, user_prompt, max_chars=6000
            )
            messages = _build_messages(system_prompt, user_prompt)

            res = client.chat.completions.create(
                model=model_name,
                messages=messages,
                response_format={"type": "json_object"},
            )
        else:
            raise

    response_text = (res.choices[0].message.content or "").strip()

    valid, data_or_error = validate_action_plan(response_text)
    if valid:
        _print_debug_json("Validated JSON response", data_or_error)
        return data_or_error

    print(f"Groq response validation failed: {data_or_error}")

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
