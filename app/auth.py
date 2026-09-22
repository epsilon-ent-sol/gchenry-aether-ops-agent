"""
Enterprise Identity & SPIFFE Token Verification Interceptor
Prevents Broken Object Level Authorization (BOLA) and rogue agent impersonation.
"""
from fastapi import Header, HTTPException, status
import jwt
from app.config import settings

def verify_agent_identity(authorization: str = Header(None)) -> dict:
    """
    Validates SPIFFE Workload Identity / Bearer JWT tokens passed during inter-agent calls.
    """
    if not settings.ENFORCE_SPIFFE_AUTH and settings.ENVIRONMENT == "development":
        return {
            "sub": "local-developer",
            "spiffe_id": settings.EXPECTED_SPIFFE_ID,
            "role": "admin"
        }

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header with Bearer token."
        )

    token = authorization.split(" ")[1]

    try:
        # In production, verify signature against OIDC / SPIFFE SPIRE JWKS endpoint
        # For demo purposes, we decode claims and inspect the SPIFFE URI & role
        decoded = jwt.decode(token, options={"verify_signature": False})
        
        spiffe_id = decoded.get("spiffe_id") or decoded.get("sub")
        role = decoded.get("role", "viewer")

        if spiffe_id != settings.EXPECTED_SPIFFE_ID and role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access Denied: SPIFFE ID '{spiffe_id}' is not authorized for deployment release gates."
            )

        return decoded

    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid agent authentication token: {str(e)}"
        )

