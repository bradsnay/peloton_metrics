from peloton_metrics.dal.peloton_api_clients.user_client import UserClient
from peloton_metrics.dal.peloton_api_clients.workout_metrics_client import (
    WorkoutMetricsClient,
)
from peloton_metrics.dal.postgres.tracked_users_dao import TrackedUsersDao
from peloton_metrics.dal.postgres.workout_dao import WorkoutDao
from peloton_metrics.exceptions.private_user_exception import PrivateUserException
from peloton_metrics.processors.base_processor import BaseProcessor
from peloton_metrics.models.user import User


class WorkoutMetricsFollowerCrawler(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.workout_client = WorkoutMetricsClient()
        self.workout_dao = WorkoutDao()
        self.user_client = UserClient(self.workout_client.api_session)
        self.seen_user_ids = set()
        self.user_dao = TrackedUsersDao()

    def run(self, user_id: str, depth: int = 1):
        """
        Recursivly find new users to track by traversing the followers + following of the given user_id.

        Run the workout refresh module to update their workouts.

        :param user_id: The user from which to start scraping users from.
        This can be thought of as the "root" of the follower graph
        :param depth: How deep down the rabbit hole to go.
        0 = just the provided user's data
        1 = the user and all of their followers/followed users
        2 = everything above plus their followers/followed users followers and followed users.
        and so on...
        :return: None
        """

        def _run_recursion_helper(user: User, depth: int):
            if depth == 0:
                return

            if user.is_profile_private is True:
                print(f"User account is private. user_id:{user.username}")
                return
            

            users = []
            users.extend(self.user_client.fetch_user_following(user.user_id))
            users.extend(self.user_client.fetch_user_followers(user.user_id))

            for user in users:
                user_id = user.user_id
                # If my followers also follow me, I'll see myself again.
                if user_id in self.seen_user_ids:
                    continue
                self.seen_user_ids.add(user_id)

                print("Saving user: ", user.username)
                self.user_dao.upsert_tracked_user(user)
                _run_recursion_helper(user, depth - 1)
    
        user = self.user_client.fetch_user_profile(user_id)
        self.user_dao.upsert_tracked_user(user)
        _run_recursion_helper(user, depth)

        print("Done! Updating tracked users.")
