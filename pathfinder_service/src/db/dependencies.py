from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.repositories.coordinates import CoordinatesRepository
from src.db.repositories.pathfinder import PathfinderRepository
from src.db.repositories.routes import RoutesRepository


# Dependency
async def get_session(request: Request) -> AsyncSession:
    async_session = request.app.state.db

    async with async_session() as session:
        yield session


async def get_coordinates_repository(
    session: AsyncSession = Depends(get_session),
) -> CoordinatesRepository:
    return CoordinatesRepository(session)


async def get_routes_repository(
    session: AsyncSession = Depends(get_session),
) -> RoutesRepository:
    return RoutesRepository(session)


async def get_pathfinder_repository(
    session: AsyncSession = Depends(get_session),
) -> PathfinderRepository:
    return PathfinderRepository(session)
