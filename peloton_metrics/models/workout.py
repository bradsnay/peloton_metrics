from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import (
    AliasChoices,
    BaseModel,
    BeforeValidator,
    Field,
    field_serializer,
    model_validator,
)

from peloton_metrics.dal.helpers.date_time_helper_functions import (
    convert_int_to_datetime,
)


class Workout(BaseModel):
    workout_id: str = Field(validation_alias=AliasChoices("id", "workout_id"))
    user_id: str
    created_at: Annotated[datetime, BeforeValidator(convert_int_to_datetime)]
    start_time: Annotated[datetime, BeforeValidator(convert_int_to_datetime)]
    end_time: Annotated[Optional[datetime], BeforeValidator(convert_int_to_datetime)]
    timezone: Optional[str]
    status: str
    device_type: str
    fitness_discipline: str
    has_pedaling_metrics: bool
    has_leaderboard_metrics: bool
    total_work: float
    is_total_work_personal_record: bool
    is_outdoor: bool
    metrics_type: Optional[str]
    name: str
    peloton_id: Optional[str]
    platform: Optional[str]
    workout_type: str
    total_watch_time_seconds: Optional[int] = Field(
        validation_alias=AliasChoices("v2_total_video_watch_time_seconds")
    )
    difficulty_rating_avg: Optional[float]
    difficulty_rating_count: Optional[int]
    difficulty_level: Optional[str]
    duration: int
    image_url: Optional[str]
    title: str
    instructor_id: Optional[str]
    instructor_first_name: Optional[str]
    instructor_last_name: Optional[str]

    @model_validator(mode="before")
    @classmethod
    def extract_nested_values(cls, data: dict) -> dict:
        ride_data = data.get("ride", dict()) or dict()
        instructor_data = ride_data.get("instructor", dict()) or dict()
        res = {
            **data,
            "difficulty_rating_avg": ride_data.get("difficulty_rating_avg"),
            "difficulty_rating_count": ride_data.get("difficulty_rating_count"),
            "difficulty_level": ride_data.get("difficulty_level"),
            "duration": ride_data.get("duration") or -1,
            "image_url": ride_data.get("image_url"),
            "title": ride_data.get("title"),
            "instructor_id": instructor_data.get("id"),
            "instructor_first_name": instructor_data.get("first_name"),
            "instructor_last_name": instructor_data.get("last_name"),
        }
        return res

    @field_serializer("created_at", "start_time", "end_time")
    def convert_datetime_to_str(
        self, model_date_value: Optional[datetime]
    ) -> Optional[str]:
        return (
            model_date_value.strftime("%Y-%m-%d %H:%M:%S.%f")
            if model_date_value is not None
            else None
        )
