"""
Workout metrics client.

Loads user configuration data (such as passwords) from files stored in the
secrets directory (not checked into git for obvious reasons).

@author Brad Snay <bradsnay@gmail.com>
"""
from peloton_metrics.dal.peloton_api_clients.peloton_api_client import PelotonApiClient
from peloton_metrics.dal.big_query.user_workout_dao import UserWorkoutDao
from peloton_metrics.dal.peloton_api_clients.user_client import UserClient
from peloton_metrics.exceptions.private_user_exception import PrivateUserException


class WorkoutMetricsClient(PelotonApiClient):

    @staticmethod
    def workout_endpoint(user_id: str):
        return f"/api/user/{user_id}/workouts"

    def fetch_all_workouts(self, user_id: str):
        user_client = UserClient(api_session=self.api_session)
        is_user_private = user_client.fetch_user_profile(user_id)['is_profile_private']
        if not is_user_private:
            return self.fetch_all(self.workout_endpoint(user_id))
        raise PrivateUserException(f"User {user_id} has a private profile. No workouts will be loaded.")

    def save_all_workouts(self, user_id: str, workout_data: list):
        user_client = UserClient(api_session=self.api_session)
        user_name = user_client.fetch_user_profile(user_id)['username']

        client = UserWorkoutDao()
        last_saved_workout_timestamp = client.fetch_most_recently_saved_workout_timestamp(user_id)

        new_workouts_to_save = []
        for workout in workout_data:
            # Only save completed workouts that we haven't already saved.
            if workout["created_at"] > last_saved_workout_timestamp and workout['status'] == 'COMPLETE':
                new_workouts_to_save.append(workout)
        if len(new_workouts_to_save) > 0:
            client.save_all_workout_data(user_name, new_workouts_to_save)
        print(f"Saved {len(new_workouts_to_save)} new workouts to BigQuery for user_id {user_id}")
