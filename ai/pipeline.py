from .tools import tool_config
from config import config
from .gemini import *
from .nvidia import *
from .groq import *
from .ollama import *
import json

def provider_init(provider_name):
    if provider_name == "gemini":
        return gemini_init()
    elif provider_name == "nvidia":
        return nvidia_init()
    elif provider_name == "groq":
        return groq_init()
    elif provider_name == "ollama":
        return ollama_init()
    else:
        raise ValueError(f"Unknown provider: {provider_name}")

def ai_pipeline(prompt):
    # Pass the prompt through various AI processing stages
    # Stage 1:
    response = analyse_prompt(prompt)
    return response

def call_provider(provider, system_prompt, user_prompt, model_name):
    print(f"Attempting inference via {provider} ({model_name})...")
    try:
        if provider == "gemini":
            response = provider_gemini(system_prompt, user_prompt, model_name)
        elif provider == "nvidia":
            response = provider_nvidia(system_prompt, user_prompt, model_name)
        elif provider == "groq":
            response = provider_groq(system_prompt, user_prompt, model_name)
        elif provider == "ollama":
            response = provider_ollama(system_prompt, user_prompt, model_name)
        else:
            response = None

        if response is None:
            print(f"Provider {provider} returned no usable response.")
        return response
    except Exception as e:
        print(f"Failed to generate content with {provider}: {str(e)}")
        return None

def analyse_prompt(prompt):
    system_prompt = """You are an AI computer agent.

Your job is to help the user by either:
1. Responding with text
2. Using tools to perform actions on the computer

You MUST decide carefully.

---

RULES:

1. If the user asks for an action (open, search, click, type, play, send, etc), you MUST use a tool.

2. If the user asks a question (what, why, explain), respond with text.
    - If you already know the answer, respond with text.
    - If the answer may require up-to-date information, external knowledge, or you are not confident, you MUST use a search tool.

    Examples of when to use search:
    - current events
    - recent information
    - specific facts you are unsure about
    - anything that might change over time

    If a search tool exists, prefer using it instead of guessing.

3. NEVER guess tool arguments.
Only use arguments that match the tool schema exactly.

4. NEVER invent tools.
Only use tools from the provided list.

5. If unsure, respond with text instead of using a tool.

6. Always choose ONE action at a time.
Do NOT combine multiple tools in one response.

7. Be simple and direct. No long explanations.

8. NEVER guess unknown facts.
If you are not sure, use a search tool instead of answering.
---

AVAILABLE TOOLS:

{tools}

---

OUTPUT FORMAT (VERY IMPORTANT):

You MUST respond in valid JSON only.

Format:

{
  "type": "tool" OR "text",
  "tool": "tool_name" OR null,
  "args": {} OR null,
  "response": "text response if type is text, otherwise null"
}

---

EXAMPLES:

User: open chrome

Output:
{
  "type": "tool",
  "tool": "open_app",
  "args": { "app_name": "chrome" },
  "response": null
}

---

User: what is AI

Output:
{
  "type": "text",
  "tool": null,
  "args": null,
  "response": "AI means artificial intelligence."
}

---

User: search for laptops

Output:
{
  "type": "tool",
  "tool": "search_browser",
  "args": { "query": "laptops" },
  "response": null
}

User: who is the current prime minister of india

Output:
{
  "type": "tool",
  "tool": "search_browser",
  "args": { "query": "current prime minister of india" },
  "response": null
}

---

IMPORTANT:

- Always return valid JSON
- Do not add extra text outside JSON
- Do not explain your reasoning
- Be accurate and minimal

Now process the user input."""

    serialized_tools = []
    for tool in tool_config:
        if hasattr(tool, "model_dump"):
            serialized_tools.append(tool.model_dump())
        elif hasattr(tool, "dict"):
            serialized_tools.append(tool.dict())
        elif isinstance(tool, dict):
            serialized_tools.append(tool)
        else:
            serialized_tools.append(str(tool))

    compiled_system_prompt = system_prompt.replace(
        "{tools}",
        json.dumps(serialized_tools, ensure_ascii=True, indent=2),
    )

    for provider in config["ai_fallback_provider_chain"]:
        # check if provider can be initialized
        try:
            provider_init(provider)
        except Exception as e:
            print(f"Error initializing provider {provider}: {str(e)}")
            continue
        model_name = config["provider_models"].get(provider)
        if model_name:
            # Call the provider with the system prompt and user prompt
            response = call_provider(provider, compiled_system_prompt, prompt, model_name)
            if response:
                return response

    return {
        "type": "text",
        "tool": None,
        "args": None,
        "response": "I could not generate a response right now. Please try again.",
    }

