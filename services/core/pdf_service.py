
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
import tempfile
import os


def load_pdf_documents(pdf_file) -> List[Document]:
    """
    Loads PDF and returns LangChain Document objects
    with page-level metadata.
    """

    # Streamlit uploads file in memory → LangChain needs file path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_path = tmp_file.name

    loader = PyPDFLoader(tmp_path)
    documents = loader.load()

    os.remove(tmp_path)

    return documents


def chunk_pdf_documents(
    documents: List[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 100,
) -> List[Document]:
    """
    Splits PDF documents into chunks while preserving metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    chunks = splitter.split_documents(documents)

    return chunks


def process_pdf(
    pdf_file,
    chunk_size: int = 800,
    chunk_overlap: int = 100,
) -> List[Document]:

    documents = load_pdf_documents(pdf_file)

    chunked_documents = chunk_pdf_documents(
        documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    return chunked_documents