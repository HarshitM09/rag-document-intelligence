from fastapi import APIRouter, Depends, HTTPException, status
from backend.models.schemas import (
    AuthRequest,
    IngestionRequest,
    SearchRequest,
    ChatRequest,
    AnalyticsResponse,
)
from backend.services.auth_service import require_api_key
from backend.services.ingestion_service import IngestionService
from backend.services.retrieval_service import RetrievalService
from backend.services.analytics_service import AnalyticsService

api_router = APIRouter()

ingestor = IngestionService()
retriever = RetrievalService()
analytics = AnalyticsService()


@api_router.post("/auth/login", tags=["auth"])
def login(request: AuthRequest):
    """Authenticate a service or user and return a scoped integration token."""
    token = require_api_key(request.api_key)
    return {"access_token": token, "token_type": "bearer"}


@api_router.post("/ingest/repository", tags=["ingestion"])
def ingest_repository(request: IngestionRequest, api_key: str = Depends(require_api_key)):
    """Ingest repository content, chunk files, and store embeddings in the vector database."""
    job_id = ingestor.ingest_repository(request)
    return {"job_id": job_id, "status": "queued", "source": request.repository_url}


@api_router.post("/search", tags=["search"])
def semantic_search(request: SearchRequest, api_key: str = Depends(require_api_key)):
    """Perform semantic retrieval across embeddings and return ranked document segments."""
    results = retriever.semantic_search(request)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No relevant vectors found")
    return results


@api_router.post("/chat", tags=["conversational"])
def conversational_query(request: ChatRequest, api_key: str = Depends(require_api_key)):
    """Orchestrate a conversational RAG workflow with semantic grounding and response generation."""
    response = retriever.conversational_response(request)
    return response


@api_router.get("/analytics/summary", response_model=AnalyticsResponse, tags=["analytics"])
def analytics_summary(api_key: str = Depends(require_api_key)):
    """Return analytical insights for ingestion and query activity."""
    return analytics.summary()