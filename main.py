from ai.pipeline import ai_pipeline
from userInteraction import get_user_input
import json


def _format_ai_output(res):
    if res is None:
        return "I could not generate a response right now."

    if isinstance(res, dict):
        response_type = res.get("type")
        if response_type == "text":
            return res.get("response") or "I could not generate a response right now."
        if response_type == "tool":
            tool_name = res.get("tool") or "unknown_tool"
            args = res.get("args") or {}
            return f"Planned action: {tool_name} with args {json.dumps(args, ensure_ascii=True)}"

    return str(res)

def loop():
    while True:
        prompt = get_user_input()
        # print(f"You asked: {prompt}")
        # Process the prompt through the AI pipeline
        res = ai_pipeline(prompt)
        print(f"AI Response: {_format_ai_output(res)}")

loop()