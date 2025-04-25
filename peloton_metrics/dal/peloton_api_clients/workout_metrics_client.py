"""
Workout metrics client.

Loads user configuration data (such as passwords) from files stored in the
secrets directory (not checked into git for obvious reasons).

@author Brad Snay <bradsnay@gmail.com>
"""

from concurrent.futures import ThreadPoolExecutor, as_completed

from peloton_metrics.dal.helpers.decorators import select_as_models
from peloton_metrics.dal.peloton_api_clients.peloton_api_client import PelotonApiClient
from peloton_metrics.dal.peloton_api_clients.user_client import UserClient
from peloton_metrics.dal.postgres.workout_dao import WorkoutDao
from peloton_metrics.exceptions.private_user_exception import PrivateUserException
from peloton_metrics.metrics_extraction.user_workout_metrics_extractor import (
    UserWorkoutMetricsExtractor,
)
from peloton_metrics.metrics_extraction.workout_performance_extractor import (
    WorkoutPerformanceExtractor,
)
from peloton_metrics.models.user import User
from peloton_metrics.models.workout import Workout
from peloton_metrics.models.workout_performance_metrics import WorkoutPerformanceMetrics


class WorkoutMetricsClient(PelotonApiClient):
    @staticmethod
    def workout_endpoint(user_id: str):
        return f"/api/user/{user_id}/workouts"

    @staticmethod
    def workout_performance_metrics_endpoint(workout_id: str) -> str:
        return f"/api/workout/{workout_id}/performance_graph?every_n=5"

    @select_as_models(Workout)
    def fetch_all_workouts(self, user: User, num_records: int = 100):
        if not user.is_profile_private:
            return self.fetch_all(
                self.workout_endpoint(user.user_id), num_records=num_records
            )
        raise PrivateUserException(
            f"User {user.user_id} has a private profile. No workouts will be loaded."
        )

    def save_all_workouts(self, user: User, workout_data: list[Workout]):

        num_workouts = user.total_workouts
        workout_dao = WorkoutDao()
        last_saved_workout_timestamp = (
            workout_dao.fetch_most_recently_saved_workout_timestamp(user.user_id)
        )

        new_workouts_to_save = []
        performance_metrics = []
        num_workouts = len(workout_data)
        futures = []
        with ThreadPoolExecutor(max_workers=10) as thread_pool:
            for i, workout in enumerate(workout_data):
                if self.is_workout_eligible_to_be_saved(
                    workout, last_saved_workout_timestamp
                ):
                    print(
                        f"Fetching performance metrics for workout: {workout.workout_id} ({i+1}/{num_workouts})"
                    )
                    futures.append(
                        thread_pool.submit(
                            self.fetch_workout_performance_metrics, workout
                        )
                    )
                    new_workouts_to_save.append(workout)

        for ft in as_completed(futures):
            metrics = ft.result()
            print(f"Received metrics for workout id {metrics.workout_id}")
            performance_metrics.append(metrics)

        if len(new_workouts_to_save) > 0:
            workout_dao.save_all_workout_data(new_workouts_to_save, performance_metrics)

        print(
            f"Saved {len(new_workouts_to_save)} new workouts for user {user.username}({user.user_id})"
        )

    def fetch_workout_performance_metrics(
        self, workout: Workout
    ) -> WorkoutPerformanceMetrics:
        return WorkoutPerformanceExtractor.extract_all_performance_metrics(
            self.request(
                self.workout_performance_metrics_endpoint(workout.workout_id)
            ).json(),
            workout_id=workout.workout_id,
        )

    @staticmethod
    def is_workout_eligible_to_be_saved(
        workout: Workout, last_saved_workout_timestamp: int
    ) -> bool:
        # Only save completed workouts that we haven't already saved.
        return (
            workout.created_at.timestamp() > last_saved_workout_timestamp
            and workout.status == "COMPLETE"
        )
