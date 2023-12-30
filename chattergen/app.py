from dotenv import load_dotenv

load_dotenv()
import os
from rich.console import Console
from rich.prompt import Prompt
from pyfiglet import Figlet
import google.generativeai as genai
from chattergen.utils import (
    create_table,
    generate_response,
    generation_config,
    safety_settings,
    inital_history,
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
genai_model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)
model = genai_model.start_chat(history=[])
console = Console()


def start():
    """Start the ChatterGen CLI."""
    f = Figlet(font="slant")
    console.print(f.renderText("ChatterGen"), style="bold green")
    console.print(
        "Welcome to ChatterGen! Type your question or prompt.", style="bold green"
    )

    while True:
        prompt = Prompt.ask("You ")
        if prompt.lower() in ["quit", "exit", "q"]:
            console.print("Exiting ChatterGen. Goodbye!", style="bold red")
            break
        console.print(create_table("Prompt", prompt))
        try:
            with console.status("[cyan]Generating response..."):
                model_response = generate_response(model, prompt)
                console.print(
                    create_table("", model_response, "green"),
                    soft_wrap=True,
                    style="bold green",
                )
        except Exception as e:
            console.print(f"Error: {e}", style="bold red")


def main():
    try:
        start()
    except KeyboardInterrupt:
        console.print("\nExiting ChatterGen. Goodbye!", style="bold red")


if __name__ == "__main__":
    main()
