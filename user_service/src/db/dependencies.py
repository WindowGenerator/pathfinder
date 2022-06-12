from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.repositories.users import UserRepository


# Dependency
async def get_session(request: Request) -> AsyncSession:
    async_session = request.app.state.db

    async with async_session() as session:
        yield session


async def get_user_repository(
    session: AsyncSession = Depends(get_session),
) -> UserRepository:
    return UserRepository(session)
