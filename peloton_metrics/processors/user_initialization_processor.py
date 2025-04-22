from peloton_metrics.dal.peloton_api_clients.user_client import UserClient
from peloton_metrics.dal.postgres.tracked_users_dao import TrackedUsersDao
from peloton_metrics.models.user import User
from peloton_metrics.processors.base_processor import BaseProcessor


class UserInitializationProcessor(BaseProcessor):

    def __init__(self):
        super().__init__()
        self.user_client = UserClient()
        self.tracked_users_dao = TrackedUsersDao()

    def run(self):
        identity = User(**self.user_client.self_identify())
        user_name = identity.username
        user_id = identity.user_id
        print(f"Tracking New User: {user_name}({user_id})")
        self.tracked_users_dao.upsert_tracked_user(identity)
        print("Done.")
