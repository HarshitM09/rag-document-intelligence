from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from backend.core.config import settings

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def require_api_key(api_key: str = Security(api_key_header)) -> str:
    """Validate the incoming API key for secure enterprise access."""
    if not api_key or api_key != f"Bearer {settings.API_KEY}":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return api_key
