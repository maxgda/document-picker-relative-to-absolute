from configuration import api_token, project_id, environment, channel
from src.constants import prefix

response_map = {
    'y': True,
    'n': False
}


def get_yes_no_input(prompt):
    while True:
        user_input = input(f"{prompt} y/n").strip().lower()
        if user_input in response_map:
            return response_map[user_input]
        else:
            print("Please enter 'y' or 'n'.")


def get_execute_script_input(prompt):
    print("verify configuration:")
    print(f"environment = {environment}")
    print(f"channel = {channel}")
    print(f"project_id = {project_id}")
    print(f"api_token = {api_token}")
    print(f"prefixed path = {prefix}")

    input(prompt)
    print("Executing...")