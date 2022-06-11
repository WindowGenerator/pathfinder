import logging
from hashlib import sha256
from typing import Dict, Optional

import jwt
from src.settings import AppSettings, get_app_settings

logger = logging.getLogger(__name__)


def sign_jwt(user_id: int) -> str:
    app_settings: AppSettings = get_app_settings()

    payload = {"user_id": user_id}
    token = jwt.encode(
        payload, app_settings.jwt_secret, algorithm=app_settings.jwt_algorithm
    )

    return token


def decode_jwt(token: str) -> Optional[Dict]:
    app_settings: AppSettings = get_app_settings()
    try:
        return jwt.decode(
            token, app_settings.jwt_secret, algorithms=[app_settings.jwt_algorithm]
        )
    except Exception as exc:
        logger.error(exc)
        return None


def hash_password(password: str) -> str:
    """
    Calculate hash from pass
    """
    return sha256(password.encode("utf-8")).hexdigest()
