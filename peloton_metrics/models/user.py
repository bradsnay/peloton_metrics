from datetime import datetime
from typing import Annotated, Optional

from pydantic import AliasChoices, BaseModel, BeforeValidator, Field, field_serializer

from peloton_metrics.dal.helpers.date_time_helper_functions import (
    convert_int_to_datetime,
)


class User(BaseModel):
    user_id: str = Field(validation_alias=AliasChoices("id", "user_id"))
    date_initialized: Annotated[
        Optional[datetime], BeforeValidator(convert_int_to_datetime)
    ] = None
    last_updated: Annotated[
        Optional[datetime], BeforeValidator(convert_int_to_datetime)
    ] = None
    username: str
    location: Optional[str] = None
    image_url: Optional[str] = None
    total_workouts: Optional[int] = 0
    is_profile_private: Optional[bool] = False
    peloton_join_date: Annotated[
        Optional[datetime], BeforeValidator(convert_int_to_datetime)
    ] = Field(alias="created_at", default=None)

    @field_serializer("date_initialized", "peloton_join_date")
    def convert_datetime_to_str(
        self, model_date_value: Optional[datetime]
    ) -> Optional[str]:
        if model_date_value is None:
            return None
        return model_date_value.strftime("%Y-%m-%d %H:%M:%S.%f")
