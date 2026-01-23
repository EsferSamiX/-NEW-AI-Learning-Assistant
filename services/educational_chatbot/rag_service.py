from typing import List, Tuple, Optional

from langchain.schema import Document

from services.core.pdf_service import process_pdf
from services.core.embedding_service import EmbeddingService
from services.core.vectorstore_service import VectorStoreService
from services.core.cache_service import CacheService
from services.core.groq_client import get_groq_response

from utils.prompt_templates import (
    RAG_ANSWER_PROMPT,
    PDF_QUESTION_GENERATION_PROMPT,
)


EMBEDDING_DIMENSION = 384


# VECTORSTORE BUILDER
def build_vectorstore_from_pdf(pdf_file) -> VectorStoreService:
    """
    Builds or retrieves a cached FAISS vector store for an uploaded PDF.
    """

    file_hash = CacheService.generate_file_hash(pdf_file)

    cached_store = CacheService.get_cached_vectorstore(file_hash)
    if cached_store:
        return cached_store

    documents: List[Document] = process_pdf(pdf_file)

    texts = [doc.page_content for doc in documents]

    embedder = EmbeddingService()
    embeddings = embedder.embed_texts(texts)

    vectorstore = VectorStoreService(
        embedding_dimension=EMBEDDING_DIMENSION
    )

    vectorstore.add_documents(
        embeddings=embeddings,
        documents=documents,
    )

    CacheService.set_cached_vectorstore(file_hash, vectorstore)

    return vectorstore



# SAFE RETRIEVAL LAYER
def retrieve_documents(
    vectorstore: VectorStoreService,
    query: str,
    top_k: int = 4,
) -> List[Document]:

    embedder = EmbeddingService()
    query_embedding = embedder.embed_query(query)

    return vectorstore.similarity_search(
        query_embedding=query_embedding,
        top_k=top_k,
    )



# RAG QUESTION ANSWERING (WITH MEMORY)
def ask_question_with_rag(
    vectorstore: VectorStoreService,
    question: str,
    top_k: int = 4,
    memory_text: Optional[str] = None,
) -> Tuple[str, List[Document]]:
    """
    Retrieval-Augmented Question Answering with conversation memory.
    """

    retrieved_docs = retrieve_documents(
        vectorstore=vectorstore,
        query=question,
        top_k=top_k,
    )

   
    # Build document context
  
    context_blocks = []

    for doc in retrieved_docs:
        page = doc.metadata.get("page", "N/A")
        content = doc.page_content.strip()

        context_blocks.append(
            f"[Page {page + 1}]\n{content}"
        )

    document_context = "\n\n".join(context_blocks)

    
    # Memory section (optional)
    
    memory_section = ""
    if memory_text:
        memory_section = f"""
Conversation so far:
{memory_text}
"""


    # Prompt
    prompt = RAG_ANSWER_PROMPT.format(
        memory_section=memory_section,
        document_context=document_context,
        question=question,
    )

    answer = get_groq_response(
        prompt=prompt,
        temperature=0.2,
    )

    return answer, retrieved_docs



# QUESTION GENERATION FROM PDF

def generate_questions_from_pdf(
    vectorstore: VectorStoreService,
    num_questions: int = 5,
) -> List[str]:
    """
    Generates exam-style questions grounded in PDF content.
    """

    docs = retrieve_documents(
        vectorstore=vectorstore,
        query="important concepts, definitions, mechanisms, explanations",
        top_k=8,
    )

    combined_text = "\n\n".join(
        d.page_content for d in docs
    )

    prompt = PDF_QUESTION_GENERATION_PROMPT.format(
        context=combined_text,
        num_questions=num_questions,
    )

    response = get_groq_response(
        prompt=prompt,
        temperature=0.35,
        max_tokens=500,
    )

    questions: List[str] = []

    for line in response.splitlines():
        line = line.strip()
        if line and line[0].isdigit():
            questions.append(
                line.split(".", 1)[1].strip()
            )

    return questions



# MULTI-QUESTION EXAM CONTEXT


def get_exam_context(
    vectorstore: VectorStoreService,
    questions: List[str],
    top_k: int = 8,
) -> str:
    """
    Retrieves shared reference context for exam evaluation.
    """

    combined_query = " ".join(questions)

    docs = retrieve_documents(
        vectorstore=vectorstore,
        query=combined_query,
        top_k=top_k,
    )

    return "\n\n".join(
        doc.page_content for doc in docs
    )



# SINGLE QUESTION CONTEXT

def get_context_text(
    vectorstore: VectorStoreService,
    query: str,
    top_k: int = 4,
) -> str:
    """
    Returns merged reference context for one question.
    """

    docs = retrieve_documents(
        vectorstore=vectorstore,
        query=query,
        top_k=top_k,
    )

    return "\n".join(
        doc.page_content for doc in docs
    )
