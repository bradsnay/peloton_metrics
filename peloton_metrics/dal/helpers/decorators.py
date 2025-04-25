from typing import List, Type

from pydantic import BaseModel
from sqlalchemy.engine.row import Row


def select_as_dictionaries(select_func: callable) -> callable:
    def wrap(*args, **kwargs) -> List[dict]:
        res = select_func(*args, **kwargs)
        if not res:
            return []
        return [row._asdict() if isinstance(row, Row) else row for row in res]

    return wrap


def select_as_models(model_type: Type[BaseModel]) -> callable:
    def func_decorator(select_func: callable) -> callable:
        def wrap(*args, **kwargs) -> List[BaseModel]:
            res = select_func(*args, **kwargs)
            if not res:
                return []
            models = []
            for i, row in enumerate(res):
                row_dict = row
                if isinstance(row, Row):
                    row_dict = row._asdict()
                models.append(model_type(**row_dict))
            return models
            # return [model_type(**(row._asdict() if isinstance(row, Row) else row)) for row in res]

        return wrap

    return func_decorator
