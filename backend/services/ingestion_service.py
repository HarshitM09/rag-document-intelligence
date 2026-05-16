import uuid
from typing import List, Dict
from backend.core.config import settings
from backend.utils.file_utils import list_text_files, read_document, chunk_text
from backend.utils.embeddings import EmbeddingEngine
from backend.utils.guardrails import enforce_document_provenance
from backend.services.analytics_service import AnalyticsService
from backend.core.logging import get_logger

logger = get_logger(__name__)


class IngestionService:
    """Responsible for repository scraping, document chunking, and embedding ingestion."""

    def __init__(self):
        self.embedding_engine = EmbeddingEngine()
        self.analytics = AnalyticsService()

    def ingest_repository(self, request: Dict[str, any]) -> str:
        source_url = request.get("repository_url")
        namespace = request.get("namespace") or "enterprise"
        index_name = request.get("index_name")

        logger.info("Beginning ingestion for source=%s index=%s namespace=%s", source_url, index_name, namespace)

        file_paths = list_text_files(source_url)
        document_chunks = self._build_document_chunks(file_paths)
        embeddings = self.embedding_engine.embed_documents(document_chunks)

        vector_payload = []
        for idx, chunk in enumerate(document_chunks):
            metadata = enforce_document_provenance({
                "document_id": f"{index_name}-{idx}",
                "source_url": source_url,
                "chunk_size": len(chunk.split()),
            })
            vector_payload.append({
                "id": f"{uuid.uuid4()}",
                "chunk": chunk,
                "embedding": embeddings[idx],
                "metadata": metadata,
            })

        self.embedding_engine.upsert_vectors(namespace, vector_payload)
        self.analytics.record_ingestion(len(vector_payload))

        job_id = str(uuid.uuid4())
        logger.info("Finished ingestion job %s with %s document vectors", job_id, len(vector_payload))
        return job_id

    def _build_document_chunks(self, file_paths: List[str]) -> List[str]:
        chunks = []
        for path in file_paths:
            content = read_document(path)
            chunks.extend(
                chunk_text(
                    content,
                    chunk_size=settings.MAX_CHUNK_SIZE,
                    overlap=settings.MIN_CHUNK_OVERLAP,
                )
            )
        logger.debug("Generated %s semantic chunks from repository sources", len(chunks))
        return chunks
