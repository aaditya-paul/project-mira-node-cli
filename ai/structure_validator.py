import json
from typing import Any, Tuple


def _extract_json_payload(response_text: str) -> str:
    text = response_text.strip()

    # Handle markdown fenced JSON output.
    if text.startswith("```"):
        lines = text.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

    # If extra text was included, try to isolate the first JSON object.
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text

def validate_action_plan(response_text: str) -> Tuple[bool, Any]:
    """
    Validates if the provided text is valid JSON and contains the required fields:
    'intent', 'target', and 'tool'.
    
    Args:
        response_text (str): The response string from the model (expected to be JSON).
        
    Returns:
        Tuple[bool, Any]: A tuple where the first element is a boolean indicating 
                          validity, and the second element is either the parsed 
                          dictionary (if valid) or an error message string (if invalid).
    """
    if response_text is None:
        return False, "Model returned no text response."

    payload = _extract_json_payload(response_text)
    if not payload:
        return False, "Model returned an empty response."

    # 1. Validate if it's JSON
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON format: {str(e)}"
        
    # 2. Check if the parsed JSON is a dictionary
    if not isinstance(data, dict):
        return False, "Parsed JSON is not a dictionary object."
        
    # 3. Check for required fields
    required_fields = {"type", "tool", "args", "response"}
    missing_fields = required_fields - data.keys()
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
        
    # 4. Validate and normalize by action type
    action_type = data.get("type")
    if action_type not in {"tool", "text"}:
        return False, "'type' must be either 'tool' or 'text'."

    if action_type == "tool":
        if not isinstance(data.get("tool"), str) or not data.get("tool").strip():
            return False, "'tool' must be a non-empty string when type is 'tool'."
        if data.get("args") is None:
            data["args"] = {}
        elif not isinstance(data.get("args"), dict):
            return False, "'args' must be an object when type is 'tool'."
        if data.get("response") is not None and not isinstance(data.get("response"), str):
            return False, "'response' must be null or a string when type is 'tool'."

    if action_type == "text":
        if not isinstance(data.get("response"), str) or not data.get("response").strip():
            return False, "'response' must be a non-empty string when type is 'text'."
        data["tool"] = None
        data["args"] = None
        
    return True, data
