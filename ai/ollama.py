from .structure_validator import validate_action_plan

def ollama_init():
    # Ollama is typically running locally, so initialization might not need an API key.
    # Return True or an ollama client instance.
    return True

def provider_ollama(system_prompt, user_prompt, model_name):
    ollama_init()
    # Use ollama python client or requests
    # import ollama
    # res = ollama.chat(
    #     model=model_name,
    #     messages=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": user_prompt}
    #     ],
    #     format="json"
    # )
    # return res['message']['content']
    pass
