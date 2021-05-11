from peloton_metrics.dal.peloton_api_clients.user_client import UserClient
from peloton_metrics.dal.big_query.tracked_users_dao import TrackedUsersDao
from peloton_metrics.dal.peloton_api_clients.workout_metrics_client import WorkoutMetricsClient


class TrackNewUserProcessor:

    def track_new_user(self, user_id_or_name: str):
        # Fetch the user's profile so we can extract their user_id and username
        user_profile = UserClient().fetch_user_profile(user_id_or_name)
        user_id = user_profile['id']
        user_name = user_profile['username']

        # Save the user id and name to our internal database so that our refresh job will pick it up.
        TrackedUsersDao().insert_new_tracked_user(user_id, user_name)

        # Save all workout data for the user for the first time.
        workout_client = WorkoutMetricsClient()
        workout_client.save_all_workouts(
            user_id,
            workout_client.fetch_all_workouts(
                user_id
            )
        )
