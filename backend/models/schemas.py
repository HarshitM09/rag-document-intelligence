from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field


class AuthRequest(BaseModel):
    api_key: str = Field(..., description="Service API key used for authentication")


class IngestionRequest(BaseModel):
    repository_url: HttpUrl = Field(..., description="Repository or document source URL for ingestion")
    index_name: str = Field(..., description="Target semantic index identifier")
    namespace: Optional[str] = Field(None, description="Optional knowledge domain or business unit namespace")


class SearchRequest(BaseModel):
    query: str = Field(..., description="Natural language search query")
    top_k: Optional[int] = Field(5, description="Number of top semantic results to return")
    filters: Optional[dict] = Field(None, description="Optional metadata filters for vector retrieval")


class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: user, system, or assistant")
    content: str = Field(..., description="Message text content")


class ChatRequest(BaseModel):
    user_id: str = Field(..., description="Identity for conversational context and audit tracking")
    conversation: List[ChatMessage] = Field(..., description="Ordered chat messages for the AI workflow")
    session_id: Optional[str] = Field(None, description="Optional session identifier for long running dialogues")


class AnalyticsResponse(BaseModel):
    ingestion_jobs: int
    active_vectors: int
    average_query_latency_ms: float
    recent_user_activity: List[str]
