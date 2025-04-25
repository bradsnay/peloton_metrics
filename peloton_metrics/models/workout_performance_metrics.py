from typing import Optional

from pydantic import BaseModel


class WorkoutPerformanceMetrics(BaseModel):

    workout_id: str
    duration: int
    total_output: Optional[int] = None
    output_unit: Optional[str] = None
    total_distance: Optional[float] = None
    distance_unit: Optional[str] = None
    total_calories: Optional[int] = None
    calories_unit: Optional[str] = None
    avg_output: Optional[int] = None
    avg_cadence: Optional[int] = None
    max_cadence: Optional[int] = None
    cadence_unit: Optional[str] = None
    avg_resistance: Optional[int] = None
    max_resistance: Optional[int] = None
    resistance_unit: Optional[str] = None
    avg_speed: Optional[float] = None
    max_speed: Optional[float] = None
    speed_unit: Optional[str] = None
