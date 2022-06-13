from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Coordinates
from src.schemas.coordinates import Coordinate as CoordinateSchema


class CoordinatesRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_raw_coordinates_by_ids(
        self, coordinate_ids: List[str]
    ) -> List[Coordinates]:
        result = await self._session.execute(
            select(Coordinates).where(Coordinates.id.in_(coordinate_ids))
        )
        await self._session.commit()

        return [coordinate for coordinate in result.scalars()]

    async def get_coordinates(
        self, number_from: int, limit: int = 100
    ) -> List[CoordinateSchema]:
        result = await self._session.execute(
            select(Coordinates).where(Coordinates.number > number_from).limit(limit)
        )
        coordinates = list()

        for coordinate in result.scalars():
            coordinates.append(
                CoordinateSchema(
                    id=str(coordinate.id),
                    name=coordinate.name,
                    x_coord=coordinate.x_coord,
                    y_coord=coordinate.y_coord,
                )
            )

        return coordinates

    async def get_length(self) -> int:
        result = await self._session.execute(
            """
            WITH tbl AS
                (
                    SELECT table_schema, table_name
                    FROM information_schema.tables
                    WHERE table_name not like 'pg_%'
                        AND table_schema in ('public')
                        AND table_name = 'coordinates'
                )
                SELECT (
                    xpath(
                        '/row/c/text()',
                        query_to_xml(
                            format('select count(*) as c from %I.%I', table_schema, table_name), FALSE, TRUE, ''
                        )
                    )
                )[1]::text::int AS rows_n
                FROM tbl
                ORDER BY rows_n DESC;
            """
        )
        (length,) = result.fetchone()

        return length

    async def get_coordinate_by_id(self, coord_id: str) -> CoordinateSchema:
        result = await self._session.execute(
            select(Coordinates).where(Coordinates.id == coord_id)
        )
        await self._session.commit()
        coord = result.scalar()

        if coord is None:
            return None

        return CoordinateSchema(
            id=str(coord.id),
            name=coord.name,
            x_coord=coord.x_coord,
            y_coord=coord.y_coord,
        )
