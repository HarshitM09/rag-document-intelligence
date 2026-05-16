import os
from typing import List, Dict
from backend.core.config import settings
from sentence_transformers import SentenceTransformer


class EmbeddingEngine:
    """Encapsulates embedding creation and vector store operations."""

    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.vector_store_path = settings.VECTOR_DB_PATH
        self.index = {}

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Generate dense embeddings for document chunks."""
        return self.model.encode(documents, show_progress_bar=False, convert_to_numpy=True).tolist()

    def upsert_vectors(self, namespace: str, items: List[Dict[str, object]]) -> None:
        """Persist vector records in a lightweight vector database abstraction."""
        if namespace not in self.index:
            self.index[namespace] = []
        self.index[namespace].extend(items)

    def semantic_search(self, namespace: str, query_embedding: List[float], top_k: int = 5):
        """Perform a simple cosine similarity search over in-memory vectors."""
        import numpy as np

        candidate_rows = self.index.get(namespace, [])
        if not candidate_rows:
            return []

        query_vector = np.array(query_embedding, dtype=float)
        scores = []
        for row in candidate_rows:
            candidate_vector = np.array(row["embedding"], dtype=float)
            similarity = float(np.dot(query_vector, candidate_vector) / (np.linalg.norm(query_vector) * np.linalg.norm(candidate_vector) + 1e-12))
            scores.append({"score": similarity, **row})

        sorted_results = sorted(scores, key=lambda row: row["score"], reverse=True)
        return sorted_results[:top_k]
