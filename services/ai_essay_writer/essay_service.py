from typing import Optional
import re

from services.core.groq_client import get_groq_response
from utils.prompt_templates import ESSAY_PROMPT
from utils.constants import DEFAULT_WORD_LIMIT, DEFAULT_TONE

# Helper functions


def _clean_outline(outline: Optional[str]) -> str:
    """
    Normalizes optional outline input.
    """
    if not outline or not outline.strip():
        return "No outline provided."

    outline = outline.strip()

    # Convert comma-separated input into bullets
    if "\n" not in outline:
        outline = "\n".join(
            f"- {point.strip()}"
            for point in outline.split(",")
            if point.strip()
        )

    return outline


def _estimate_token_limit(word_limit: int) -> int:
    """
    Token buffer to avoid sentence truncation.
    """
    return int(word_limit * 2.0)



# Main service


def generate_essay(
    topic: str,
    word_limit: Optional[int] = None,
    tone: Optional[str] = None,
    outline: Optional[str] = None,
) -> str:
    """
    Generates a structured academic essay.
    """

    
    # Defaults
    
    final_word_limit = (
        word_limit if word_limit and word_limit > 0 else DEFAULT_WORD_LIMIT
    )

    final_tone = tone if tone else DEFAULT_TONE
    cleaned_outline = _clean_outline(outline)

    max_tokens = _estimate_token_limit(final_word_limit)

    
    # Build prompt from template
    
    prompt = ESSAY_PROMPT.format(
        topic=topic,
        tone=final_tone,
        word_limit=final_word_limit,
        outline=cleaned_outline,
    )

    
    # LLM call
    
    essay = get_groq_response(
        prompt=prompt,
        temperature=0.7,
        max_tokens=max_tokens,
    )

    
    # Post-processing
    
    essay = re.sub(r"\n{3,}", "\n\n", essay).strip()

    return essay
