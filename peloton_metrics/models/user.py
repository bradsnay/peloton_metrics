from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, Field, field_serializer


def convert_int_to_datetime(raw_int: Optional[int]) -> datetime:
    if raw_int is None:
        return None
    return datetime.fromtimestamp(raw_int)


class User(BaseModel):
    user_id: str = Field(alias="id")
    date_initialized: Annotated[
        Optional[datetime], BeforeValidator(convert_int_to_datetime)
    ] = None
    last_updated: Optional[int] = None
    username: str
    first_name: str
    last_name: str
    location: Optional[str] = None
    image_url: Optional[str] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    weight_unit: Optional[str] = None
    height: Optional[float] = None
    height_unit: Optional[str] = None
    total_workouts: int = 0
    peloton_join_date: Annotated[
        Optional[datetime], BeforeValidator(convert_int_to_datetime)
    ] = Field(alias="created_at")
    birthday: Annotated[
        Optional[datetime], BeforeValidator(convert_int_to_datetime)
    ] = None

    @field_serializer("date_initialized", "peloton_join_date", "birthday")
    def convert_datetime_to_str(
        self, model_date_value: Optional[datetime]
    ) -> Optional[str]:
        if model_date_value is None:
            return None
        return model_date_value.strftime("%Y-%m-%d %H:%M:%S.%f")
