from typing import Any, List
from pydantic import BaseModel, Field, validator
from rpi_ws281x import Color
from datetime import datetime, timedelta


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

    def add_minutes(self, n):
        """Add n minutes to the start_time."""
        # Parse the start_time string to a datetime object
        start_time_dt = datetime.strptime(self.start_time, "%H:%M:%S")
        # Add n minutes
        new_time = start_time_dt + timedelta(minutes=n)
        # Return the new time as a string
        return new_time.strftime("%H:%M:%S")

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
    fill_light: Any
    cyc: List[SegColor3] = Field(..., description="An array of 5 SegmentColor3 models")

    @validator("cyc")
    def validate_cyc_length(cls, value):
        if len(value) != 5:
            raise ValueError("The 'cyc' field must contain exactly 5 SegmentColor3 models")
        return value