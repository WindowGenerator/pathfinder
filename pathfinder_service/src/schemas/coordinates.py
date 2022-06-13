from pydantic import BaseModel, Field


class CoordinateID(BaseModel):
    id: str = Field(...)


class Coordinate(CoordinateID):
    id: str = Field(...)
    name: str = Field(...)

    x_coord: float = Field(...)
    y_coord: float = Field(...)
