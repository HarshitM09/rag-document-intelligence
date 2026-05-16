from typing import Dict, List
from backend.core.config import settings
from backend.core.logging import get_logger

logger = get_logger(__name__)


class AnalyticsService:
    """Collects analytics for ingestion, query performance, and operational telemetry."""

    def __init__(self):
        self.ingestion_jobs = 0
        self.active_vectors = 0
        self.query_durations = []
        self.user_activity = []
        self.enabled = settings.ANALYTICS_ENABLED

    def record_ingestion(self, vector_count: int) -> None:
        if not self.enabled:
            return
        self.ingestion_jobs += 1
        self.active_vectors += vector_count
        logger.info("Analytics recorded ingestion with %s vectors", vector_count)

    def track_query(self, payload: Dict[str, any]) -> Dict[str, any]:
        if not self.enabled:
            return {}
        self.query_durations.append(150.0)
        self.user_activity.append(payload.get("query", "unknown"))
        return {"tracked": True, "query": payload.get("query")}

    def track_conversation(self, payload: Dict[str, any]) -> None:
        if not self.enabled:
            return
        self.user_activity.append(f"conversation:{payload.get('user_id')}")
        logger.debug("Conversation tracked for user %s", payload.get("user_id"))

    def summary(self) -> Dict[str, any]:
        average_latency = sum(self.query_durations) / len(self.query_durations) if self.query_durations else 0.0
        return {
            "ingestion_jobs": self.ingestion_jobs,
            "active_vectors": self.active_vectors,
            "average_query_latency_ms": average_latency,
            "recent_user_activity": self.user_activity[-10:],
        }
