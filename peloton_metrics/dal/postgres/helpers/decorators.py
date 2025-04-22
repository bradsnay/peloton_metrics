from typing import List


def select_as_dictionaries(select_func: callable) -> callable:
    def wrap(*args, **kwargs) -> List[dict]:
        res = select_func(*args, **kwargs)
        if not res:
            return []
        return [row._asdict() for row in res]

    return wrap
