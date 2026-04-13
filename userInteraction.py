def get_user_input():
    print("Hi! I am Mira - your personal assistant agent. How can I help you today?")
    prompt = input("Ask me anything: ")
    check_commands(prompt)
    return prompt


def check_commands(prompt):
    # EXIT PHRASES
    if prompt.lower() in ["exit", "quit", "bye"]:
        exit_program()
    # Add more command checks here as needed


def exit_program():
    print("Goodbye! Have a great day!")
    exit()

