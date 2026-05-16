from typing import Dict, Any
from backend.services.ingestion_service import IngestionService
from backend.services.retrieval_service import RetrievalService
from backend.services.analytics_service import AnalyticsService
from backend.core.logging import get_logger

logger = get_logger(__name__)


class Orchestrator:
    """Orchestrates enterprise AI workflows across ingestion, retrieval, and analytics."""

    def __init__(self):
        self.ingestion = IngestionService()
        self.retrieval = RetrievalService()
        self.analytics = AnalyticsService()

    def run_ingestion_pipeline(self, request: Dict[str, Any]) -> str:
        """Run the repository ingestion pipeline end-to-end."""
        logger.info("Starting ingestion pipeline for repository: %s", request.get("repository_url"))
        job_id = self.ingestion.ingest_repository(request)
        logger.debug("Ingestion job created: %s", job_id)
        return job_id

    def run_search_workflow(self, query_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate semantic retrieval and ranking for a user query."""
        logger.info("Executing search workflow for query: %s", query_payload.get("query"))
        results = self.retrieval.semantic_search(query_payload)
        metadata = self.analytics.track_query(query_payload)
        return {"results": results, "metadata": metadata}

    def run_conversational_flow(self, conversation_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate conversational AI with grounding, prompt orchestration, and guardrails."""
        logger.info("Processing conversational request for user_id: %s", conversation_payload.get("user_id"))
        response = self.retrieval.conversational_response(conversation_payload)
        self.analytics.track_conversation(conversation_payload)
        return response
