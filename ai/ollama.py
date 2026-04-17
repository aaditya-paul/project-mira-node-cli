from .structure_validator import validate_action_plan
import json
import ollama


def _print_debug_json(label, payload):
    print(f"{label}:")
    print(json.dumps(payload, ensure_ascii=True, indent=2))


def _ensure_json_instruction(system_prompt):
    if "json" not in system_prompt.lower():
        system_prompt += "\n\nReturn ONLY valid JSON. Do not include explanations."
    return system_prompt


def _shorten_context(system_prompt, user_prompt, max_chars=10000):
    sys_max = int(max_chars * 0.4)
    usr_max = int(max_chars * 0.6)

    short_system = system_prompt[:sys_max]

    if len(user_prompt) > usr_max:
        short_user = user_prompt[:usr_max] + "\n...[truncated]"
    else:
        short_user = user_prompt

    return short_system, short_user


def ollama_init():
    # Local, nothing fancy needed
    return True


def provider_ollama(system_prompt, user_prompt, model_name, structured_output=True):
    ollama_init()

    if structured_output:
        # ✅ enforce JSON behavior
        system_prompt = _ensure_json_instruction(system_prompt)

    # ✅ trim context (same strategy as Groq)
    system_prompt, user_prompt = _shorten_context(system_prompt, user_prompt)

    request_kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
    }
    if structured_output:
        request_kwargs["format"] = "json"

    try:
        res = ollama.chat(**request_kwargs)
    except Exception as e:
        print(f"Ollama request failed: {e}")
        return None

    response_text = (res.get("message", {}).get("content", "") or "").strip()

    if not structured_output:
        if response_text:
            return response_text
        return None

    valid, data_or_error = validate_action_plan(response_text)
    if valid:
        _print_debug_json("Validated JSON response", data_or_error)
        return data_or_error

    print(f"Ollama response validation failed: {data_or_error}")

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