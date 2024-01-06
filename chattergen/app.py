from dotenv import load_dotenv

load_dotenv()
import sys
from rich.console import Console
from rich.prompt import Prompt
from pyfiglet import Figlet
import google.generativeai as genai
from chattergen.utils import (
    create_table,
    generate_response,
    generation_config,
    safety_settings,
    process_args,
    read_config_file,
    get_training_data,
)


def create_model(api_key: str):
    genai.configure(api_key=api_key)
    genai_model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    return genai_model.start_chat(history=[])

console = Console()


def start():
    """Start the ChatterGen CLI."""

    print("\033c")

    f = Figlet(font="slant")
    console.print(f.renderText("ChatterGen"), style="bold green")
    if len(sys.argv) > 1:
        process_args(sys.argv)
    model = create_model(read_config_file())
    console.print(
        "Welcome to ChatterGen! Type your question or prompt.", style="bold green"
    )

    training_data = get_training_data()
    if training_data:
        generate_response(
            model,
            get_training_data(),
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
            console.print(
                f"Error: Some error occured.Try another prompt", style="bold red"
            )


def main():
    try:
        start()
    except KeyboardInterrupt:
        console.print("\nExiting ChatterGen. Goodbye!", style="bold red")


if __name__ == "__main__":
    main()
