from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.auth.helpers import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)

        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=403, detail="Invalid authentication scheme."
            )
        if decode_jwt(credentials.credentials) is None:
            raise HTTPException(
                status_code=403, detail="Invalid token or expired token."
            )

        return credentials.credentials
