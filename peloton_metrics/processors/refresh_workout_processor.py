from peloton_metrics.dal.peloton_api_clients.workout_metrics_client import (
    WorkoutMetricsClient,
)
from peloton_metrics.dal.postgres.tracked_users_dao import TrackedUsersDao
from peloton_metrics.exceptions.private_user_exception import PrivateUserException
from peloton_metrics.processors.base_processor import BaseProcessor


class RefreshWorkoutProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.tracked_users_dao = TrackedUsersDao()
        self.workout_client = WorkoutMetricsClient()

    def run(self):
        print(f"------Refreshing workouts started------")
        # TODO: Use a generator to load these iteratively.
        tracked_users = self.tracked_users_dao.fetch_tracked_users()
        for user in tracked_users:
            user_id = user["user_id"]
            print(f"Updating metrics for user id: {user_id}")
            try:
                workouts = self.workout_client.fetch_all_workouts(user_id)
                self.workout_client.save_all_workouts(user_id, workouts)
            except PrivateUserException:
                print(f"User account is private. user_id:{user_id}")
        print(f"------Refreshing workouts ended------")
