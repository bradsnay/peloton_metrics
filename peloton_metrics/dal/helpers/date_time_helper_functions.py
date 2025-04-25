from datetime import datetime
from typing import Optional


def convert_int_to_datetime(raw_int: Optional[int]) -> Optional[datetime]:
    if raw_int is None:
        return None
    if isinstance(raw_int, datetime):
        return raw_int
    return datetime.fromtimestamp(raw_int)
