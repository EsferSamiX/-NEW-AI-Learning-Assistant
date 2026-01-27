from typing import Optional, List
import re

from langchain_text_splitters import RecursiveCharacterTextSplitter

from services.core.groq_client import get_groq_response
from services.core.pdf_service import load_pdf_documents

from utils.prompt_templates import (
    SHORT_SUMMARY_PROMPT,
    BULLET_SUMMARY_PROMPT,
    FINAL_BULLET_MERGE_PROMPT,
    FINAL_PARAGRAPH_MERGE_PROMPT,
)

from services.ai_text_summarization.summarization_utils import (
    estimate_token_limit,
    clean_text,
)



# INTERNAL HELPERS


def _summarize_chunks(
    chunks: List[str],
    mode: str,
    max_words: Optional[int],
) -> str:
    """
    Summarizes multiple text chunks and merges results.
    """

    partial_summaries = []

    for chunk in chunks:
        summary = summarize_text(
            text=chunk,
            mode=mode,
            max_words=max_words,
        )
        partial_summaries.append(summary)

    combined = "\n".join(partial_summaries)

    # --------------------------------------------------
    # Final merge stage
    # --------------------------------------------------

    if mode == "bullet":
        final_prompt = FINAL_BULLET_MERGE_PROMPT.format(
            summaries=combined
        )
    else:
        final_prompt = FINAL_PARAGRAPH_MERGE_PROMPT.format(
            summaries=combined
        )

    final_summary = get_groq_response(
        prompt=final_prompt,
        temperature=0.3,
        max_tokens=estimate_token_limit(
            max_words if max_words else 300
        ),
    )

    return final_summary.strip()



# TEXT SUMMARIZATION


def summarize_text(
    text: str,
    mode: str = "short",
    max_words: Optional[int] = None,
) -> str:
    """
    Summarizes pasted text.
    """

    if not text or not text.strip():
        raise ValueError("Input text is empty.")

    cleaned_text = clean_text(text)

    system_prompt = (
        BULLET_SUMMARY_PROMPT
        if mode == "bullet"
        else SHORT_SUMMARY_PROMPT
    )

    word_instruction = (
        f"Limit the summary to approximately {max_words} words."
        if max_words
        else "Be concise while preserving key meaning."
    )

    prompt = f"""
{system_prompt}

{word_instruction}

Text:
\"\"\"
{cleaned_text}
\"\"\"
"""

    max_tokens = estimate_token_limit(
        max_words if max_words else 250
    )

    summary = get_groq_response(
        prompt=prompt,
        temperature=0.3,
        max_tokens=max_tokens,
    )

    summary = re.sub(r"\n{3,}", "\n\n", summary).strip()

    return summary



# PDF SUMMARIZATION


def summarize_pdf(
    pdf_file,
    mode: str = "short",
    max_words: Optional[int] = None,
) -> str:
    """
    Summarizes uploaded PDF content.
    """

    documents = load_pdf_documents(pdf_file)

    full_text = "\n".join(
        doc.page_content for doc in documents
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150,
    )

    chunks = splitter.split_text(full_text)

    return _summarize_chunks(
        chunks=chunks,
        mode=mode,
        max_words=max_words,
    )
