from rich.table import Table
from rich.markdown import Markdown
from google.generativeai import ChatSession

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
inital_history= "Your name is ChatterGen, and you are a chatbot that uses the Gemini Pro model from Google's GenerativeAI API."
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
