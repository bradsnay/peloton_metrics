from peloton_metrics.dal.peloton_api_clients.user_client import UserClient
from peloton_metrics.dal.peloton_api_clients.workout_metrics_client import (
    WorkoutMetricsClient,
)
from peloton_metrics.dal.postgres.tracked_users_dao import TrackedUsersDao
from peloton_metrics.dal.postgres.workout_dao import WorkoutDao
from peloton_metrics.exceptions.private_user_exception import PrivateUserException
from peloton_metrics.processors.base_processor import BaseProcessor


class RefreshWorkoutProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.tracked_users_dao = TrackedUsersDao()
        self.workout_client = WorkoutMetricsClient()
        self.user_client = UserClient()
        self.workout_dao = WorkoutDao()

    def run(self):
        print(f"------Refreshing workouts started------")
        # TODO: Use a generator to load these iteratively.
        tracked_users = self.tracked_users_dao.fetch_tracked_users()
        for user in tracked_users:
            user_id = user.user_id
            saved_workout_count = self.workout_dao.fetch_saved_workout_count(user_id)
            peloton_user = self.user_client.fetch_user_profile(user_id)

            self.tracked_users_dao.upsert_tracked_user(peloton_user)
            workout_count_diff = peloton_user.total_workouts - saved_workout_count

            # TODO: This doesn't account for workout deletions. We'll figure that out at some point.
            if workout_count_diff == 0:
                print(
                    f"{user.username} hasn't worked out since last refresh. Skipping..."
                )
                continue

            print(
                f"Updating metrics on {workout_count_diff} workouts for user: {user.username}({user_id})"
            )
            try:
                workouts = self.workout_client.fetch_all_workouts(
                    peloton_user, num_records=workout_count_diff
                )
                self.workout_client.save_all_workouts(peloton_user, workouts)
            except PrivateUserException:
                print(f"User account is private. user_id:{user_id}")
        print(f"------Refreshing workouts ended------")
