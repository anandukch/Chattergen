import os
from setuptools import setup, find_packages

setup(
    name="chattergen",
    version="0.1.0",
    description="A simple chatbot that uses the Gemini Pro model from Google's GenerativeAI API",
    author="Anandu",
    py_modules="ChatterGen",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "rich",
        "google-generativeai",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "chattergen=chattergen.app:main",
        ]
    },
)
