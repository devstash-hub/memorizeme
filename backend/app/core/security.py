from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user_id(credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)) -> str:
    """
    Validates the Supabase Auth JWT Bearer token and returns the authenticated user's UUID (sub).
    In local development without a configured JWT secret, falls back to a development user.
    """
    if not credentials:
        # Development fallback if token is omitted in local dev
        if settings.SUPABASE_JWT_SECRET in ("", "your-supabase-jwt-secret"):
            return "00000000-0000-0000-0000-000000000001"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Bearer authentication token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    # If secret is placeholder or omitted, decode without verification for dev/testing
    if settings.SUPABASE_JWT_SECRET in ("", "your-supabase-jwt-secret"):
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return str(payload.get("sub", "00000000-0000-0000-0000-000000000001"))
        except Exception:
            return "00000000-0000-0000-0000-000000000001"

    try:
        # Standard Supabase JWT verification
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            options={"verify_aud": False},
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject (sub) claim.",
            )
        return str(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
        )
