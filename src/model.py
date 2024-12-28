from typing import Any, List
from pydantic import BaseModel, Field, validator
from rpi_ws281x import Color
from datetime import datetime, timedelta

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
    lamps_on: bool
    fill_light: List[tuple]
    cyc: List[tuple] = Field(..., description="An array of 5 color tuples")

    @validator("cyc")
    def validate_cyc_length(cls, value):
        if len(value) != 5:
            raise ValueError("The 'cyc' field must contain exactly 5 color tuples")
        return value

class Step(BaseModel):
    time: str
    lamps_on: bool = False
    phase_name: str
    fill_light: List[tuple]
    cyc: List[tuple] = Field(..., description="An array of 5 color tuples")

    @validator("cyc")
    def validate_cyc_length(cls, value):
        if len(value) != 5:
            raise ValueError("The 'cyc' field must contain exactly 5 color tuples")
        return value
