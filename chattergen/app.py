from dotenv import load_dotenv

load_dotenv()
import os

from rich.table import Table
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from pyfiglet import Figlet
import google.generativeai as genai

# Set up the model
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

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)
console = Console()


class ChatterGenState:
    def __init__(self) -> None:
        self.chat_history = []

    def add_to_history(self, user_input: str, model_resposne: str) -> None:
        self.chat_history.append((user_input, model_resposne))

    def get_history(self) -> list:
        return self.chat_history


chatter_gen_state = ChatterGenState()


def generate_response(prompt: str) -> tuple:
    context = "\n".join([f"{x[0]}>{x[1]}" for x in chatter_gen_state.get_history()])
    res = model.generate_content(context + prompt)
    return Markdown(res.text), res.text


def create_table(title: str, text: str,color:str="magenta"):
    table = Table(title=title, show_header=False, padding=(1, 1, 1, 1), min_width=10)
    table.add_column("You", style=color)
    table.add_row(text)
    return table


def start():
    """Start the ChatterGen CLI."""
    f = Figlet(font="slant")
    console.print(f.renderText("ChatterGen"), style="bold green")
    console.print(
        "Welcome to ChatterGen! Type your question or prompt.", style="bold green"
    )
    table = Table(title="ChatterGen", show_header=False, padding=(1, 1, 1, 1))
    table.add_column("You", style="magenta")
    table.add_row("What is the meaning of life?")

    while True:
        prompt = Prompt.ask("You ")
        if prompt.lower() in ["quit", "exit", "q"]:
            console.print("Exiting ChatterGen. Goodbye!")
            break
        console.print(create_table("Prompt", prompt))
        try:
            with console.status("[cyan]Generating response..."):
                model_response = generate_response(prompt)
                console.print(create_table("",model_response[0],"green"), soft_wrap=True, style="bold green")
                chatter_gen_state.add_to_history(prompt, model_response[1])
        except Exception as e:
            console.print(f"Error: {e}", style="bold red")
        
        # empty_table = Table(show_header=False, width=Console().width,style="bold red",title_justify="center"

def main():
    try:
        start()
    except KeyboardInterrupt:
        console.print("Exiting ChatterGen. Goodbye!")

if __name__ == "__main__":
    main()
