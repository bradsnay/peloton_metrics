"""
Workout metrics client.

Loads user configuration data (such as passwords) from files stored in the
secrets directory (not checked into git for obvious reasons).

@author Brad Snay <bradsnay@gmail.com>
"""

from peloton_metrics.dal.peloton_api_clients.peloton_api_client import PelotonApiClient
from peloton_metrics.dal.peloton_api_clients.user_client import UserClient
from peloton_metrics.dal.postgres.user_workout_dao import UserWorkoutDao
from peloton_metrics.exceptions.private_user_exception import PrivateUserException
from peloton_metrics.metrics_extraction.user_workout_metrics_extractor import (
    UserWorkoutMetricsExtractor,
)
from peloton_metrics.metrics_extraction.workout_performance_extractor import (
    WorkoutPerformanceExtractor,
)


class WorkoutMetricsClient(PelotonApiClient):
    @staticmethod
    def workout_endpoint(user_id: str):
        return f"/api/user/{user_id}/workouts"

    @staticmethod
    def workout_performance_metrics_endpoint(workout_id: str) -> str:
        return f"/api/workout/{workout_id}/performance_graph"

    def fetch_workout_performance_metrics(self, workout_id: str):
        performance_metrics = self.request(
            self.workout_performance_metrics_endpoint(workout_id)
        ).json()
        return performance_metrics

    def fetch_all_workouts(self, user_id: str):
        user_client = UserClient(api_session=self.api_session)
        is_user_private = user_client.fetch_user_profile(user_id)["is_profile_private"]
        if not is_user_private:
            return self.fetch_all(self.workout_endpoint(user_id))
        raise PrivateUserException(
            f"User {user_id} has a private profile. No workouts will be loaded."
        )

    def save_all_workouts(self, user_id: str, workout_data: list):
        user_client = UserClient(api_session=self.api_session)
        user_name = user_client.fetch_user_profile(user_id)["username"]

        user_workout_dao = UserWorkoutDao()
        last_saved_workout_timestamp = (
            user_workout_dao.fetch_most_recently_saved_workout_timestamp(user_id)
        )

        metrics_extractor = UserWorkoutMetricsExtractor()
        new_workouts_to_save = []
        for workout in workout_data:
            if self.is_workout_eligible_to_be_saved(
                workout, last_saved_workout_timestamp
            ):
                new_workouts_to_save.append(
                    self.enrich_workout_with_performance_metrics(
                        metrics_extractor.extract_one(workout, user_name=user_name)
                    )
                )

        if len(new_workouts_to_save) > 0:
            user_workout_dao.save_all_workout_data(new_workouts_to_save)

        print(
            f"Saved {len(new_workouts_to_save)} new workouts to BigQuery for user_id {user_id}"
        )

    def enrich_workout_with_performance_metrics(self, workout: dict) -> dict:
        performance_data = self.fetch_workout_performance_metrics(workout["id"])
        extracted_performance_data = (
            WorkoutPerformanceExtractor.extract_all_performance_metrics(
                performance_data
            )
        )
        return {**workout, **extracted_performance_data}

    @staticmethod
    def is_workout_eligible_to_be_saved(
        workout: dict, last_saved_workout_timestamp: int
    ) -> bool:
        # Only save completed workouts that we haven't already saved.
        return (
            workout["created_at"] > last_saved_workout_timestamp
            and workout["status"] == "COMPLETE"
        )
