import httpx
from fastapi import Request, HTTPException
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


URL = "http://user_service:3777/api/v1/auth/check"


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        await self._check_auth(request)
    
    async def _check_auth(self, request: Request) -> None:
        headers = {}
        if "Authorization" in request.headers:
            headers={"Authorization": request.headers["Authorization"]}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(URL, headers=headers)

            if response.status_code != 200:
                body = response.json()
                raise HTTPException(
                    response.status_code,
                    detail=body["detail"]
                )
