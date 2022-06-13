from fastapi import APIRouter, Depends
from src.auth.bearer import JWTBearer
from src.auth.helpers import decode_jwt
from src.db.dependencies import get_user_repository
from src.db.repositories.users import UserRepository
from src.schemas.users import User, UserFromDBSchema

router = APIRouter(prefix="/users")


@router.get("/me", response_model=User, name="users:get-user-by-email")
async def current_user(
    access_token: JWTBearer = Depends(JWTBearer()),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    """
    Returns the current user
    """

    decoded_token = decode_jwt(access_token)
    user: UserFromDBSchema = await user_repository.get_user_by_id(
        decoded_token["user_id"]
    )

    return User(id=user.id, email=user.email, username=user.username)
