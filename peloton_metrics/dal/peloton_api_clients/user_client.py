from peloton_metrics.dal.helpers.decorators import select_as_models
from peloton_metrics.dal.peloton_api_clients.peloton_api_client import PelotonApiClient
from peloton_metrics.models.user import User


class UserClient(PelotonApiClient):

    @staticmethod
    def self_identify_endpoint() -> str:
        return "/api/me"

    @staticmethod
    def user_endpoint(user_id: str) -> str:
        return f"/api/user/{user_id}"

    @staticmethod
    def user_followers_endpoint(user_id: str) -> str:
        return f"/api/user/{user_id}/followers"

    @staticmethod
    def user_following_endpoint(user_id: str) -> str:
        return f"/api/user/{user_id}/following"

    def self_identify(self) -> User:
        return User(**self.request(self.self_identify_endpoint()).json())

    def fetch_user_profile(self, user_id: str) -> User:
        return User(**self.request(self.user_endpoint(user_id)).json())

    @select_as_models(User)
    def fetch_user_followers(self, user_id: str):
        users = self.fetch_all(self.user_followers_endpoint(user_id))
        return users

    @select_as_models(User)
    def fetch_user_following(self, user_id: str):
        users = self.fetch_all(self.user_following_endpoint(user_id))
        return users
