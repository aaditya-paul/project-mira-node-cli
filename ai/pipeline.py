from config import config
from .gemini import gemini_init, provider_gemini
from .nvidia import nvidia_init, provider_nvidia
from .groq import groq_init, provider_groq
from .ollama import ollama_init, provider_ollama
import json
import re
from .tools import ALL_TOOLS


PROVIDER_INITIALIZERS = {
    "gemini": gemini_init,
    "nvidia": nvidia_init,
    "groq": groq_init,
    "ollama": ollama_init,
}

PROVIDER_RUNNERS = {
    "gemini": provider_gemini,
    "nvidia": provider_nvidia,
    "groq": provider_groq,
    "ollama": provider_ollama,
}

MESSAGE_PLACEHOLDER_PATTERN = re.compile(
    r"<\s*generate\s+message\s+about\s+(.+?)\s*>",
    flags=re.IGNORECASE,
)


def _extract_contact_name_from_prompt(prompt):
    # Try to capture the recipient from phrases like "send ... to rajdeep ...".
    match = re.search(r"\bto\s+(.+)$", prompt, flags=re.IGNORECASE)
    if not match:
        return None

    tail = match.group(1).strip()
    tail = re.split(r"\b(saying|that|message|msg|about|with)\b|[,.!?;:]", tail, maxsplit=1, flags=re.IGNORECASE)[0]
    contact_name = tail.strip(" \"'")

    if not contact_name:
        return None
    if len(contact_name.split()) > 3:
        return None

    return contact_name

# TODO to be removed
def _normalize_tool_args(response, user_prompt):
    if not isinstance(response, dict):
        return response

    if response.get("type") != "tool":
        return response

    if response.get("tool") != "send_whatsapp_message":
        return response

    args = response.get("args")
    if not isinstance(args, dict):
        args = {}

    if args.get("phone_number") or args.get("contact_name"):
        return response

    contact_name = _extract_contact_name_from_prompt(user_prompt)
    if contact_name:
        args["contact_name"] = contact_name
        response["args"] = args
        print(f"Normalized WhatsApp recipient from prompt: contact_name='{contact_name}'")

    return response


def _extract_response_text(response):
    if isinstance(response, str):
        cleaned = response.strip()
        if cleaned.startswith('"') and cleaned.endswith('"'):
            cleaned = cleaned[1:-1].strip()
        return cleaned or None

    if isinstance(response, dict):
        response_text = response.get("response")
        if isinstance(response_text, str):
            cleaned = response_text.strip()
            return cleaned or None

    return None


def _replace_message_placeholders(command):
    # Deterministic fallback when model output is unavailable.
    def _placeholder_to_text(match):
        topic = (match.group(1) or "").strip().rstrip(".!? ")
        if not topic:
            return "Hey, just checking in."
        return f"Hey, just wanted to share that {topic}."

    return MESSAGE_PLACEHOLDER_PATTERN.sub(_placeholder_to_text, command)


def provider_init(provider_name):
    initializer = PROVIDER_INITIALIZERS.get(provider_name)
    if not initializer:
        raise ValueError(f"Unknown provider: {provider_name}")
    return initializer()

def ai_pipeline(prompt, structured_output=True):
    # Pass the prompt through various AI processing stages
    
    # Stage 1: Figure out what the user is asking for and decide on an action plan (tool use or text response)
    usr_intent = recognise_intent_and_plan(prompt, structured_output=False)
    if not isinstance(usr_intent, str) or not usr_intent.strip():
        usr_intent = prompt if isinstance(prompt, str) else ""

    # Stage 2: Handle Content Generation if needed (e.g. generate message content for texting/searching/etc)
    res_stg2 = content_generate(usr_intent, structured_output=False)
    if not isinstance(res_stg2, str) or not res_stg2.strip():
        res_stg2 = usr_intent

    # Stage 3:
    response = analyse_prompt(res_stg2, structured_output=structured_output)
    return response

def call_provider(provider, system_prompt, user_prompt, model_name, structured_output=True):
    print(f"Attempting inference via {provider} ({model_name})...")

    runner = PROVIDER_RUNNERS.get(provider)
    if runner is None:
        print(f"Provider {provider} is not supported.")
        return None

    try:
        response = runner(
            system_prompt,
            user_prompt,
            model_name,
            structured_output=structured_output,
        )

        if response is None:
            print(f"Provider {provider} returned no usable response.")
        return response
    except Exception as e:
        print(f"Failed to generate content with {provider}: {str(e)}")
        return None

def _run_provider_fallback_chain(system_prompt, user_prompt, structured_output=True):
    providers = config.get("ai_fallback_provider_chain", [])
    provider_models = config.get("provider_models", {})

    for provider in providers:
        # check if provider can be initialized
        try:
            provider_init(provider)
        except Exception as e:
            print(f"Error initializing provider {provider}: {str(e)}")
            continue

        model_name = provider_models.get(provider)
        if not model_name:
            print(f"No configured model found for provider {provider}.")
            continue

        # Call the provider with the system prompt and user prompt
        response = call_provider(
            provider,
            system_prompt,
            user_prompt,
            model_name,
            structured_output=structured_output,
        )
        if response:
            if structured_output and isinstance(user_prompt, str):
                # TODO to be removed
                return _normalize_tool_args(response, user_prompt)
            return response

    return None

def analyse_prompt(prompt, structured_output=True):
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

9. DEFAULT TOOLS TO USE UNLESS SPECIFIED:
    FOR TEXTING WHATSAPP
    FOR SEARCHING BROWSER BRAVE
---

AVAILABLE TOOLS:

{ALL_TOOLS}

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

    system_prompt = system_prompt.replace(
        "{ALL_TOOLS}",
        json.dumps(ALL_TOOLS, ensure_ascii=True, indent=2),
    )

    response = _run_provider_fallback_chain(
        system_prompt,
        prompt,
        structured_output=structured_output,
    )
    if response:
        return response


    return {
        "type": "text",
        "tool": None,
        "args": None,
        "response": "I could not generate a response right now. Please try again.",
    }

def recognise_intent_and_plan(prompt, structured_output=False):
    system_prompt = """
You are an AI assistant whose job is to convert a user's natural language input into a concise, standardized command.

Your goal is to:
- Remove unnecessary words
- Preserve full intent and all important details
- Convert the input into a clear, actionable instruction

---

RULES:

1. INTENT NORMALIZATION:
- Rewrite the user's request as a direct command.
- Do not ask questions or add extra commentary.

---

2. ACTION STANDARDIZATION:
Use consistent phrasing:

- Messaging:
  "send a whatsapp message to <contact> <message>"

- Web Search:
  "search for <query> on duckduckgo using brave browser"

- Local File Search:
  "search for <file/query> in local files"

- Open:
  "open <app/website/file>"

- Media:
  "play <media> on youtube"

- Information:
  "get information about <topic>"

---

3. LOCAL vs INTERNET DECISION:

Decide intelligently based on context:

→ Use LOCAL FILE SEARCH when:
- user mentions: "my file", "my folder", "download", "pdf", "document", "notes", "on my computer", "locally"
- or when the query clearly refers to personal/system files

→ Use WEB SEARCH when:
- query is general knowledge, products, tutorials, trends, or anything not tied to user's device

→ If unclear:
- default to WEB SEARCH

---

4. DEFAULTS:

If platform is not specified:
- texting → whatsapp
- browser → brave browser
- search engine → duckduckgo
- media → youtube

---

5. MESSAGE / CONTENT HANDLING:

- If user provides exact text → include it directly
- If user gives only a topic → use placeholder:

Format:
<generate message about ...>

Examples:
- "text rajdeep about meeting at 8pm"
  → "send a whatsapp message to rajdeep <generate message about meeting at 8pm>"

- "text rajdeep you are amazing"
  → "send a whatsapp message to rajdeep you are amazing"

---

6. PRESERVE DETAILS:

- Do not omit names, time, files, or key info
- Keep it short but complete

---

7. NON-ACTION QUERIES:

- Keep as concise question

Example:
"what's the weather like today"
→ "what is the weather today"

---

OUTPUT FORMAT:

Return ONLY the final rephrased command.
Do NOT explain anything.

---

EXAMPLES:

Input: "can you please open google chrome for me"
Output: "open chrome"

Input: "search for best laptops"
Output: "search for best laptops on duckduckgo using brave browser"

Input: "find my resume pdf"
Output: "search for resume pdf in local files"

Input: "open my downloaded assignment"
Output: "open downloaded assignment"

Input: "where is my notes file"
Output: "search for notes file in local files"

Input: "how to build a website"
Output: "search for how to build a website on duckduckgo using brave browser"

Input: "text rajdeep about how he is a good boy"
Output: "send a whatsapp message to rajdeep <generate message about how he is a good boy>"

Input: "play iris"
Output: "play iris on youtube"

Input: "what is AI"
Output: "what is AI"
"""
    response = _run_provider_fallback_chain(
        system_prompt,
        prompt,
        structured_output=structured_output,
    )
    if response:
        print(f"Intent recognition and planning successful: {response}")
        return response

    # Safe fallback to keep downstream stages operational.
    if isinstance(prompt, str):
        print("Intent recognition fallback used: returning original prompt.")
        return prompt.strip()
    return ""



def content_generate(command, structured_output=False):
    if not isinstance(command, str):
        return command

    command = command.strip()
    if not command:
        return command

    # Nothing to generate if there are no placeholders.
    if "<generate" not in command.lower():
        return command

    system_prompt = """
You are an AI assistant that fills placeholders inside a concise command.

Your task:
- Replace placeholder text like <generate message about ...> with a natural message.
- Keep the original command structure and intent unchanged.

RULES:
1. Return ONLY the final completed command text.
2. Do not add explanations, markdown, or extra lines.
3. Preserve names, times, and all key details from the command.
4. If the command has no placeholders, return it exactly as-is.
5. Keep output on a single line.

EXAMPLES:
Input: send a whatsapp message to rajdeep <generate message about meeting at 8pm>
Output: send a whatsapp message to rajdeep Hey Rajdeep, just a reminder that we are meeting at 8pm.

Input: search for <generate message about best python project ideas>
Output: search for best python project ideas
"""

    response = _run_provider_fallback_chain(
        system_prompt,
        command,
        structured_output=structured_output,
    )

    response_text = _extract_response_text(response)
    print(f"Content generation result: {response_text}")
    if response_text:
        return response_text
    
    return _replace_message_placeholders(command)