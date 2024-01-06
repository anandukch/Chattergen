from rich.table import Table
from rich.markdown import Markdown
from google.generativeai import ChatSession
from pathlib import Path
import os
import json

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

initial_prompt = "Hi! I'm ChatterGen, a chatbot that uses the Gemini Pro model from Google's GenerativeAI API. Type your question or prompt."
inital_history = "Your name is ChatterGen, and you are a chatbot that uses the Gemini Pro model from Google's GenerativeAI API."


def create_table(title: str, text: str, color: str = "magenta"):
    table = Table(title=title, show_header=False, padding=(1, 1, 1, 1), min_width=10)
    table.add_column("You", style=color)
    table.add_row(text)
    return table


def generate_response(model: ChatSession, prompt: str) -> str:
    model_res = model.send_message(prompt, stream=True)
    res = ""
    for chunk in model_res:
        res += chunk.text
    return Markdown(res)


def get_config_file() -> str:
    """Get the path to the config file."""
    home_dir = str(Path.home())
    chattergen_dir = os.path.join(home_dir, "chattergen")
    os.makedirs(chattergen_dir, exist_ok=True)
    config_file = os.path.join(chattergen_dir, "config")
    return config_file


def read_config_file() -> str:
    """Read the config file."""
    config_file = get_config_file()
    with open(config_file, "r") as file:
        content = file.read()
    return content


def is_config_empty(file_path) -> bool:
    with open(file_path, "r") as file:
        content = file.read()
        if content.strip():
            return False
        else:
            return True


def delete_file_content(file_path: str) -> None:
    with open(file_path, "w") as file:
        file.truncate(0)


def store_file_content(file_path: str, content: str) -> str:
    with open(file_path, "w") as f:
        f.write(content)
    return content


def help():
    print("ChatterGen CLI")
    print("Usage: chattergen [command] [arguments]")
    print("Commands:")
    print("    help: Show this help message")
    print("    add: Add your Google API key")
    print("    remove: Remove your Google API key")
    print("    reset: Reset your Google API key")

    exit(0)


def add_key():
    key = input("Enter your Google API key: ")
    if key:
        store_file_content(get_config_file(), key)
        print("Key added successfully!")
    else:
        print("Please enter a valid key.")


def remove_key():
    delete_file_content(get_config_file())
    print("Key removed successfully!")
    exit(0)


def reset_key():
    remove_key()
    add_key()


arg_dict = {"help": help, "add": add_key, "remove": remove_key, "reset": reset_key}


def process_args(args: list):
    if is_config_empty(get_config_file()):
        print("Please add your Google API key to use ChatterGen.")
        add_key()
    else:
        arg = args[1]
        if arg in arg_dict:
            arg_dict[arg]()
        else:
            print("Invalid command. Use 'chattergen help' to see the list of commands.")
            exit(1)


def get_training_data():
    with open("train.json", "r") as file:
        content = json.load(file)
    return json.dumps(content)

