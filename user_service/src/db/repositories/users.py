from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import User
from src.schemas.users import UserFromDBSchema


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user_by_email(self, email: str) -> Optional[UserFromDBSchema]:
        result = await self._session.execute(select(User).where(User.email == email))
        # FIXME(разобраться): await session.execute запускает неявную транзакцию????
        await self._session.commit()
        user = result.scalar()

        if user is None:
            return None

        return UserFromDBSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
        )

    async def get_user_by_id(self, user_id: str) -> Optional[UserFromDBSchema]:
        result = await self._session.execute(select(User).where(User.id == user_id))
        # FIXME(разобраться): await session.execute запускает неявную транзакцию????
        await self._session.commit()
        user = result.scalar()

        if user is None:
            return None

        return UserFromDBSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
        )
