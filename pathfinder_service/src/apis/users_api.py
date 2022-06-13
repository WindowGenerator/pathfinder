from typing import Dict

import httpx
from fastapi import HTTPException, Request
from src.settings import get_user_service_settings

user_service_settings = get_user_service_settings()

CHECK_AUTH_URL = f"{user_service_settings.user_service_url}/auth/check"
GET_CURRENT_USER_URL = f"{user_service_settings.user_service_url}/users/me"


class UsersApi:
    def _get_auth_headers(self, request: Request) -> Dict:
        headers = {}
        if "Authorization" in request.headers:
            headers = {"Authorization": request.headers["Authorization"]}

        return headers

    async def check_auth(self, request: Request) -> None:
        headers = self._get_auth_headers(request)

        async with httpx.AsyncClient() as client:
            response = await client.post(CHECK_AUTH_URL, headers=headers)

            if response.status_code != 200:
                body = response.json()
                raise HTTPException(response.status_code, detail=body["detail"])

    async def get_current_user(self, request: Request) -> Dict:
        headers = self._get_auth_headers(request)

        async with httpx.AsyncClient() as client:
            response = await client.get(GET_CURRENT_USER_URL, headers=headers)

            if response.status_code != 200:
                body = response.json()
                raise HTTPException(response.status_code, detail=body["detail"])

            return response.json()
