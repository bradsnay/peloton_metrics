from peloton_metrics.dal.peloton_api_clients.user_client import UserClient
from peloton_metrics.dal.peloton_api_clients.workout_metrics_client import (
    WorkoutMetricsClient,
)
from peloton_metrics.dal.postgres.tracked_users_dao import TrackedUsersDao
from peloton_metrics.exceptions.private_user_exception import PrivateUserException
from peloton_metrics.processors.base_processor import BaseProcessor


class WorkoutMetricsFollowerCrawler(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.workout_client = WorkoutMetricsClient()
        self.user_client = UserClient(self.workout_client.api_session)
        self.seen_user_ids = set()

    def run(self, user_id: str, depth: int = 1):
        """
        :param user_id: The user from which to start scraping workouts from.
        This can be thought of as the "root" of the follower graph
        :param depth: How deep down the rabbit hole to go.
        0 = just the provided user's data
        1 = the users data and all of their followers/followed users
        2 = everything above plus their followers/followed users followers and followed users.
        and so on...
        :return: None
        """

        def _run_recursion_helper(user_id: str, depth: int):
            if depth < 0:
                return

            try:
                self.workout_client.save_all_workouts(
                    user_id, self.workout_client.fetch_all_workouts(user_id)
                )
            except PrivateUserException:
                print(f"User account is private. user_id:{user_id}")
                return

            users = []
            users.extend(self.user_client.fetch_user_following(user_id))
            users.extend(self.user_client.fetch_user_followers(user_id))

            for user in users:
                user_id = user["id"]
                # If my followers also follow me, I'll see myself again.
                if user_id in self.seen_user_ids:
                    continue
                self.seen_user_ids.add(user_id)
                _run_recursion_helper(user_id, depth - 1)

        self._run_recursion_helper(user_id, depth)

        print("Done! Updating tracked users.")
        TrackedUsersDao().update_tracked_users()
