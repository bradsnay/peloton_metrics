from peloton_metrics.dal.big_query.tracked_users_dao import TrackedUsersDao
from peloton_metrics.dal.peloton_api_clients.workout_metrics_client import WorkoutMetricsClient
from peloton_metrics.exceptions.private_user_exception import PrivateUserException


class RefreshWorkoutProcessor:
    def __init__(self):
        self.tracked_users_dao = TrackedUsersDao()
        self.workout_client = WorkoutMetricsClient()

    def run(self):
        tracked_users = self.tracked_users_dao.fetch_tracked_users()
        for user in tracked_users:
            user_id = user['user_id']
            print(f"Updating metrics for user id: {user_id}")
            try:
                self.workout_client.save_all_workouts(
                    user_id,
                    self.workout_client.fetch_all_workouts(
                        user_id
                    )
                )
            except PrivateUserException:
                print(f"User account is private. user_id:{user_id}")
                return
