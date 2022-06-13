from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from src.apis.users_api import UsersApi

URL = "http://user_service:3777/api/v1/auth/check"


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, users_api: UsersApi = Depends(UsersApi)):
        await users_api.check_auth(request)
