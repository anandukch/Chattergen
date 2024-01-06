import google.generativeai as genai
from google.generativeai import GenerativeModel
import os
from pathlib import Path


class Chattergen(GenerativeModel):
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        super().__init__(
            model_name="gemini-pro",
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
        )
        self.start_chat(history=[])

    def generate(self, prompt):
        return self.send_message(prompt, stream=True)

    def get_config_file() -> str:
        """Get the path to the config file."""
        home_dir = str(Path.home())
        chattergen_dir = os.path.join(home_dir, "chattergen")
        os.makedirs(chattergen_dir, exist_ok=True)
        config_file = os.path.join(chattergen_dir, "config")
        return config_file

    def __call__(self, prompt):
        return self.generate(prompt)
