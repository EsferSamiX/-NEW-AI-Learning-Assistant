# pylint: disable=E1120

from typing import List
import faiss
import numpy as np
from langchain.schema import Document


class VectorStoreService:
    def __init__(self, embedding_dimension: int):
        self.index = faiss.IndexFlatIP(embedding_dimension)
        self.documents: List[Document] = []

    def add_documents(self, embeddings: List[List[float]], documents: List[Document]):
        vectors = np.asarray(embeddings, dtype="float32")
        self.index.add(vectors)
        self.documents.extend(documents)

    def similarity_search(self, query_embedding: List[float], top_k: int = 4):
        if self.index.ntotal == 0:
            return []

        query_vector = (
            np.asarray(query_embedding, dtype="float32")
            .reshape(1, -1)
        )

        scores, indices = self.index.search(query_vector, top_k)

        return [
            self.documents[i]
            for i in indices[0]
            if 0 <= i < len(self.documents)
        ]
