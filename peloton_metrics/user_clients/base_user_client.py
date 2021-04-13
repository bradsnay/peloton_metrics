"""
Base user API client.

Loads user configuration data (such as passwords) from files stored in the
user_configs directory (not checked into git for obvious reasons).

The files in the user_configs directory should be named as such "<user_name>.json".

@author Brad Snay <bradsnay@gmail.com>
"""
from abc import ABC, abstractmethod
from peloton_metrics.peloton_api_client import PelotonApiClient
import json


class BaseUserClient(ABC, PelotonApiClient):

    def __init__(self):
        self.user_name = self.get_user_name()
        self.user_config = self.load_user_config()
        self.password = self.user_config["password"]
        super().__init__(user_name=self.user_name, password=self.password)

    @abstractmethod
    def get_user_name(self) -> str:
        pass

    def workout_endpoint(self):
        return f"/api/user/{self.user_id}/workouts"

    def load_user_config(self) -> dict:
        with open(f"./user_configs/{self.get_user_name()}.json") as file:
            return json.load(file)

    def fetch_all_workouts(self):
        params = {
            'page': 0,
            'limit': 10,
            'joins': 'ride,ride.instructor'
        }
        all_workouts = []
        response = self.request(self.workout_endpoint(), **params).json()

        workout_data = response["data"]
        all_workouts.extend(workout_data)

        for i in range(1, response['page_count']):
            params['page'] += 1
            response = self.request(self.workout_endpoint(), **params).json()
            workout_data = response["data"]
            all_workouts.extend(workout_data)

        return all_workouts
