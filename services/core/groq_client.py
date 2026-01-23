

import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


DEFAULT_MODEL = "llama-3.3-70b-versatile"


def get_groq_client():
    api_key = (
        st.secrets.get("GROQ_API_KEY")
        or os.getenv("GROQ_API_KEY")
    )

    if not api_key:
        raise RuntimeError(
            "Groq API key not found.\n"
            "Add it to Streamlit Secrets or .env file."
        )

    return Groq(api_key=api_key)


def get_groq_response(
    prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
    max_tokens: int = 800,
) -> str:
    """
    Sends prompt to Groq LLM and returns response text.
    """

    client = get_groq_client()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful educational assistant."
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content.strip()


def test_groq_connection():
    client = get_groq_client()

    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: Groq connection successful."
            }
        ],
        temperature=0,
        max_tokens=20,
    )

    return response.choices[0].message.content.strip()
