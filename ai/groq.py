from .structure_validator import validate_action_plan
from dotenv import load_dotenv
import os

load_dotenv()

def groq_init():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment")
    # Initialize your groq client here (e.g. from groq import Groq)
    return api_key

def provider_groq(system_prompt, user_prompt, model_name):
    client = groq_init()
    # Stub implementation. Replace with actual library call.
    # res = client.chat.completions.create(
    #     model=model_name,
    #     messages=[{"role":"system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
    #     response_format={"type": "json_object"}
    # )
    # return res.choices[0].message.content
    pass
