from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class SearchResult(BaseModel):
    document_id: str
    score: float
    snippet: str
    metadata: Dict[str, Any]


class RetrievalResponse(BaseModel):
    query: str
    results: List[SearchResult]
    ranking_strategy: str
    source_trace: Optional[List[str]]


class ChatResponse(BaseModel):
    user_id: str
    session_id: str
    answer: str
    references: List[Dict[str, Any]]
    provenance: Optional[str]
