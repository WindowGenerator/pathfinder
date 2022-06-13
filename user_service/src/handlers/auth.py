from fastapi import APIRouter, Depends, HTTPException
from src.auth.bearer import JWTBearer
from src.auth.helpers import hash_password, sign_jwt
from src.db.dependencies import get_user_repository
from src.db.repositories.users import UserRepository
from src.schemas.users import (User, UserFromDBSchema, UserLoginSchema,
                               UserWithTokenSchema)

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=UserWithTokenSchema, name="auth:login")
async def login(
    user_input: UserLoginSchema,
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserWithTokenSchema:
    """
    User login method
    """

    user_from_db: UserFromDBSchema = await user_repository.get_user_by_email(
        user_input.email
    )

    if not user_from_db:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    hashed_password = hash_password(user_input.password)

    if not hashed_password == user_from_db.hashed_password:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = sign_jwt(user_from_db.id)

    return UserWithTokenSchema(
        user=User(
            id=user_from_db.id,
            username=user_from_db.username,
            email=user_from_db.email,
        ),
        access_token=token,
    )


@router.post(
    "/check", dependencies=[Depends(JWTBearer())], name="auth:check-auth-token"
)
async def check() -> None:
    """
    Method for check auth of user
    """
    return "Ok"
