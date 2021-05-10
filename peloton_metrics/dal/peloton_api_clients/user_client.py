from peloton_metrics.dal.peloton_api_clients.peloton_api_client import PelotonApiClient


class UserClient(PelotonApiClient):

    @staticmethod
    def user_endpoint(user_id: str) -> str:
        return f"/api/user/{user_id}"

    @staticmethod
    def user_followers_endpoint(user_id: str) -> str:
        return f"/api/user/{user_id}/followers"

    @staticmethod
    def user_following_endpoint(user_id: str) -> str:
        return f"/api/user/{user_id}/following"

    def fetch_user_profile(self, user_id: str):
        return self.request(self.user_endpoint(user_id)).json()

    def fetch_user_followers(self, user_id: str):
        return self.fetch_all(self.user_followers_endpoint(user_id))

    def fetch_user_following(self, user_id: str):
        return self.fetch_all(self.user_following_endpoint(user_id))
