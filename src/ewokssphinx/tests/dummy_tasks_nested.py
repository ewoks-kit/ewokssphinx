from typing import Literal

from ewokscore import Task
from ewokscore.model import BaseInputModel
from ewokscore.model import BaseOutputModel
from pydantic import BaseModel
from pydantic import Field


class Coordinates(BaseModel):
    planet: str = "Earth"
    latitude: int = Field(examples=[-90, 0, 90])
    longitude: float = Field(
        description="Longitude of the GPS point. **In degrees.**", examples=[-90, 0, 90]
    )


class Location(BaseModel):
    location: str = Field(
        ..., description="Name of the closest city or location to the given coordinates"
    )


class Inputs(BaseInputModel):
    coordinates: Coordinates
    vehicle: Literal["car", "bike", "bus"] = "car"


class Outputs(BaseOutputModel):
    location: Location | Coordinates
    time: str


class ComputeTimeToGo(Task, input_model=Inputs, output_model=Outputs):
    pass
