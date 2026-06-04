from ewokscore import Task
from ewokscore.model import BaseInputModel
from ewokscore.model import BaseOutputModel
from pydantic import Field


class Inputs(BaseInputModel):
    planet: str = "Earth"
    latitude: int = Field(examples=[-90, 0, 90])
    longitude: float = Field(
        description="Longitude of the GPS point. **In degrees.**", examples=[-90, 0, 90]
    )


class Outputs(BaseOutputModel):
    location: str = Field(
        ..., description="Name of the closest city or location to the given coordinates"
    )
    error: Exception | None
    is_land: bool = Field(examples=[True, False])
    languages: list[str] | None = Field(
        examples=[None, ["english"], ["english", "chinese", "hindi", "spanish"]]
    )
    uuid: bytes | None = Field(
        examples=[None, b"abcdefghijklmnopqrstuvwxyz0123456789876543210"]
    )
    metadata: dict = Field(
        description="Key-value extra information",
        examples=[
            {
                "uuid": "abcdefghijklmnopqrstuv",
                "altitude": 100,
            },
        ],
    )


class FindLocation(
    Task,
    input_model=Inputs,
    output_model=Outputs,
):
    """Finds a location given the GPS coordinates"""

    def run(self):
        pass
