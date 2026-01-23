from typing import List
from langchain.schema import Document


def generate_citations(
    documents: List[Document],
    max_snippet_length: int = 200,
) -> List[str]:
    """
    Generates human-readable citations from retrieved PDF chunks.

    Example:
    📄 Page 3 — "Self-attention allows the model to..."
    """

    citations: List[str] = []
    seen_pages = set()

    for doc in documents:

        metadata = doc.metadata or {}
        page = metadata.get("page")

        if page is None:
            continue

        if page in seen_pages:
            continue

        seen_pages.add(page)

        text = (
            doc.page_content
            .replace("\n", " ")
            .replace("  ", " ")
            .strip()
        )

        snippet = (
            text[:max_snippet_length].rstrip() + "..."
            if len(text) > max_snippet_length
            else text
        )

        citations.append(
            f"📄 Page {page + 1} — \"{snippet}\""
        )

    return citations
