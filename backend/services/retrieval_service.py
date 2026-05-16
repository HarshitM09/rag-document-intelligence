from typing import Dict, Any, List
from backend.utils.embeddings import EmbeddingEngine
from backend.utils.guardrails import validate_search_payload
from backend.services.analytics_service import AnalyticsService
from backend.core.logging import get_logger

logger = get_logger(__name__)


class RetrievalService:
    """Provides semantic retrieval, ranking, and conversational orchestration."""

    def __init__(self):
        self.engine = EmbeddingEngine()
        self.analytics = AnalyticsService()

    def semantic_search(self, request: Dict[str, Any]) -> Dict[str, Any]:
        validate_search_payload(request)
        query = request.get("query")
        top_k = request.get("top_k", 5)
        namespace = request.get("namespace", "enterprise")

        query_embedding = self.engine.model.encode([query], show_progress_bar=False, convert_to_numpy=True)[0].tolist()
        hits = self.engine.semantic_search(namespace, query_embedding, top_k=top_k)
        self.analytics.track_query({"query": query})

        return {
            "query": query,
            "results": [
                {
                    "document_id": hit["id"],
                    "score": hit["score"],
                    "snippet": hit["chunk"],
                    "metadata": hit["metadata"],
                }
                for hit in hits
            ],
            "metadata": {
                "ranking_strategy": "cosine_similarity",
                "returned": len(hits),
            },
        }

    def conversational_response(self, request: Dict[str, Any]) -> Dict[str, Any]:
        conversation = request.get("conversation", [])
        user_id = request.get("user_id")
        session_id = request.get("session_id") or "session-unknown"
        last_message = conversation[-1]["content"] if conversation else ""

        logger.info("Starting conversational retrieval flow for user %s", user_id)
        query_embedding = self.engine.model.encode([last_message], show_progress_bar=False, convert_to_numpy=True)[0].tolist()
        hits = self.engine.semantic_search("enterprise", query_embedding, top_k=4)

        answer = self._compile_response(last_message, hits)
        self.analytics.track_conversation({"user_id": user_id, "session_id": session_id})

        return {
            "user_id": user_id,
            "session_id": session_id,
            "answer": answer,
            "references": [hit["metadata"] for hit in hits],
            "provenance": "semantic retrieval + prompt orchestration",
        }

    def _compile_response(self, question: str, hits: List[Dict[str, Any]]) -> str:
        """Compose a response from retrieved document chunks and system prompt logic."""
        if not hits:
            return "No relevant enterprise documents were found for that request. Please refine your question."

        snippets = "\n---\n".join([hit["chunk"] for hit in hits])
        response = (
            f"Based on the enterprise knowledge graph and semantic index, the most relevant information is:\n\n"
            f"{snippets}\n\n"
            f"Please verify these snippets against the source documents for audit compliance."
        )
        return response
