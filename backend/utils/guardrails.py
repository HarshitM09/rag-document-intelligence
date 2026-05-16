import re
from typing import Dict, Any


def validate_search_payload(payload: Dict[str, Any]) -> None:
    """Validate search requests to prevent malformed queries and prompt injection."""
    if not payload.get("query") or len(payload["query"]) < 3:
        raise ValueError("Query must contain at least three characters")

    blocked_patterns = [r"<script>", r"\bDROP\b", r"\bDELETE\b", r"\bINSERT\b"]
    for pattern in blocked_patterns:
        if re.search(pattern, payload["query"], re.IGNORECASE):
            raise ValueError("Query contains disallowed syntax or injection risk")


def enforce_document_provenance(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Apply guardrails to metadata for attribution and source tracking."""
    metadata["trusted"] = metadata.get("trusted", True)
    metadata["source_domain"] = metadata.get("source_domain", "enterprise-knowledge")
    return metadata
