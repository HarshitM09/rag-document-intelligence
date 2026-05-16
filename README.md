# RAG Document Intelligence

## Overview

Enterprise-grade document intelligence for semantic retrieval, conversational AI, and retrieval-augmented generation (RAG).
This repository simulates a production-style architecture that indexes organizational knowledge, orchestrates vector workflows, and exposes secure APIs for analytics and search.

## Key Capabilities

- Repository scraping and document ingestion
- Content chunking and context window management
- Embedding generation with Sentence Transformers
- Vector database abstraction and semantic similarity search
- Conversational retrieval workflows with prompt orchestration
- Guardrails for input validation and provenance
- Authentication and operational analytics

## Architecture

- `backend/app.py` - FastAPI service entrypoint with health and API routes.
- `backend/api/routes.py` - API routing for auth, ingestion, search, chat, and analytics.
- `backend/services` - Business logic for ingestion, retrieval, authentication, and analytics.
- `backend/core` - Configuration, logging, and workflow orchestration.
- `backend/utils` - Document utilities, embeddings, and semantic guardrails.
- `frontend` - Minimal React interface to demonstrate search and conversational AI calls.
- `docs/architecture.md` - Technical architecture documentation.

## Getting Started

1. Copy `.env.example` to `.env` and customize environment variables.
2. Install backend dependencies:

```bash
pip install -r requirements.txt
```

3. Start the API server:

```bash
uvicorn backend.app:app --reload --port 8000
```

4. Start the front-end app (if using React tooling):

```bash
cd frontend
npm install
npm start
```

## Example API Endpoints

- `POST /v1/auth/login` - Authenticate using API key
- `POST /v1/ingest/repository` - Begin repository ingestion and embedding ingestion
- `POST /v1/search` - Perform semantic search over indexed documents
- `POST /v1/chat` - Execute conversational RAG workflow
- `GET /v1/analytics/summary` - Retrieve ingestion and query analytics

## Environment Configuration

The repository includes `.env.example` for environment variables such as:

- `API_KEY`
- `VECTOR_DB_PATH`
- `EMBEDDING_MODEL`
- `MAX_CHUNK_SIZE`
- `MIN_CHUNK_OVERLAP`
- `ANALYTICS_ENABLED`
- `LOG_LEVEL`

## Notes

This repository is intentionally medium-sized and focused on realism rather than production completeness. It is designed to illustrate architectural patterns for semantic retrieval, vector embeddings, knowledge orchestration, and enterprise-grade API workflows.
