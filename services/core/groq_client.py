import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from typing import Optional

load_dotenv()



# Configuration


DEFAULT_MODEL = "llama-3.3-70b-versatile"



# Client loader


def get_groq_client() -> Groq:
    """
    Returns Groq client using Streamlit secrets or .env.

    Priority:
    1. Streamlit Cloud secrets
    2. Local .env file
    """

    api_key = (
        st.secrets.get("GROQ_API_KEY")
        or os.getenv("GROQ_API_KEY")
    )

    if not api_key:
        raise RuntimeError(
            "Groq API key not found.\n"
            "Add GROQ_API_KEY to Streamlit Secrets or .env file."
        )

    return Groq(api_key=api_key)



# Core LLM call handler


def get_groq_response(
    prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
    max_tokens: int = 800,
) -> str:
    """
    Sends prompt to Groq LLM and returns safe response text.

    Global error handling:
    - Daily token limit exceeded
    - Rate limiting
    - Network failure
    - Timeout
    - Unexpected API crashes
    """

    try:
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


    # GROQ QUOTA / RATE LIMIT HANDLING


    except Exception as e:
        error_text = str(e).lower()

        # Daily usage / quota exceeded
        if (
            "rate limit" in error_text
            or "quota" in error_text
            or "token" in error_text
            or "maximum" in error_text
            or "429" in error_text
        ):
            return (
                "⚠️ Sorry, the Groq API maximum daily token usage has been reached. "
                "Please try again later after 24 Hours to reset the limit."
            )

        # Network / timeout issues
        if (
            "timeout" in error_text
            or "connection" in error_text
            or "network" in error_text
            or "unreachable" in error_text
        ):
            return (
                "⚠️ The AI service is temporarily unreachable. "
                "Please check your internet connection and try again."
            )

        # Unknown failure (safe fallback)
        return (
            "⚠️ An unexpected error occurred while contacting the AI service. "
            "Please try again later."
        )



# Connection test utility


def test_groq_connection() -> str:
    """
    Simple connectivity test for setup verification.
    """

    try:
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

    except Exception as e:
        return f"Groq connection failed: {str(e)}"
