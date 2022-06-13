from typing import List

from pydantic import BaseModel, Field

CoordinateID = str


class CoordinateIDs(BaseModel):
    coordinate_ids: List[CoordinateID] = Field(...)


class Coordinate(BaseModel):
    id: CoordinateID = Field(...)
    name: str = Field(...)

    x_coord: float = Field(...)
    y_coord: float = Field(...)
