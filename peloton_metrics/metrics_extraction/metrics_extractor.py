from abc import ABC, abstractmethod
from copy import deepcopy


class MetricsExtractor(ABC):

    @staticmethod
    @abstractmethod
    def included_metrics() -> set:
        pass

    def extract_metrics(self, data: list, **kwargs) -> list:
        extracted_metrics = []
        for item in data:
            # Deep copy additional hard coded row values to create a new reference.
            # Otherwise we'll end up inserting duplicate rows.
            row = deepcopy(kwargs)
            for column in self.included_metrics():
                row[column] = self._fetch_value(column, item)
            extracted_metrics.append(row)
        return extracted_metrics

    def _fetch_value(self, column_key: str, workout: dict):
        keys = column_key.split('__')
        return self._fetch_value_recursive(keys, workout)

    def _fetch_value_recursive(self, keys: list, workout: dict):
        if len(keys) == 0 or workout is None:
            return str(workout)
        if keys[0] in workout:
            return self._fetch_value_recursive(keys[1:], workout[keys[0]])