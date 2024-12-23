from typing import Any, List
from pydantic import BaseModel, Field, validator
from rpi_ws281x import Color


class SegColor3(BaseModel):
    red: int = Field(..., ge=0, le=255, description="Color value between 0 and 255")
    green: int = Field(..., ge=0, le=255, description="Color value between 0 and 255")
    blue: int = Field(..., ge=0, le=255, description="Color value between 0 and 255")

    def to_tuple(self) -> tuple:
        """Return the red, green, and blue values as a tuple."""
        return (self.red, self.green, self.blue)

class Phase(BaseModel):
    name: str
    start_time: str
    lamps_on: bool = False
    total_minutes: int

class PhaseColor(BaseModel):
    name: str
    lamps_on: bool = False
    fill_light: tuple
    cyc: List[SegColor3] = Field(..., description="An array of 5 SegmentColor3 models")

    @validator("cyc")
    def validate_cyc_length(cls, value):
        if len(value) != 5:
            raise ValueError("The 'cyc' field must contain exactly 5 SegmentColor3 models")
        return value

class Step(BaseModel):
    time: str
    lamps_on: bool = False
    fill_light: Color
    cyc: List[SegColor3] = Field(..., description="An array of 5 SegmentColor3 models")

    @validator("cyc")
    def validate_cyc_length(cls, value):
        if len(value) != 5:
            raise ValueError("The 'cyc' field must contain exactly 5 SegmentColor3 models")
        return value