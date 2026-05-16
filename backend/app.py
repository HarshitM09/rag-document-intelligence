from fastapi import FastAPI
from backend.api.routes import api_router
from backend.core.config import settings
from backend.core.logging import configure_logging

configure_logging()

app = FastAPI(
    title="Enterprise Document Intelligence API",
    version="0.1.0",
    description="A retrieval-augmented generation platform for semantic document search, indexing, and conversational AI.",
)
app.include_router(api_router, prefix="/v1")


@app.on_event("startup")
async def startup_event():
    # Startup hooks can initialize vector DB connections, analytics, and AI orchestration.
    app.state.environment = settings.ENVIRONMENT
    app.state.max_context_tokens = settings.MAX_CONTEXT_TOKENS
    app.state.vector_store = None
    app.state.analytics_enabled = settings.ANALYTICS_ENABLED


@app.get("/health", tags=["health"])
def health_check():
    """Health endpoint for monitoring and uptime checks."""
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "service": "rag-document-intelligence",
    }
