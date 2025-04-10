"""
The main Peloton API client.

@author Brad Snay <bradsnay@gmail.com>
"""

import json

import requests
from requests.auth import HTTPBasicAuth


class PelotonApiClient:

    # Base URL for all endpoints.
    BASE_URL = "https://api.onepeloton.com"

    # Let Peloton Engineers know who we are.
    USER_AGENT = "https://github.com/snayski/peloton_metrics"

    # Login endpoint for creating our session.
    AUTH_LOGIN_ENDPOINT = "/auth/login"

    # Static request headers.
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": USER_AGENT,
    }

    def __init__(self, api_session=None):
        self.api_session = api_session
        self.authorized_user_id = None
        if self.api_session is None:
            self._create_authenticated_api_session()

    def _generate_full_uri(self, endpoint: str) -> str:
        return f"{self.BASE_URL}{endpoint}"

    def load_auth_config(self) -> dict:
        with open(f"./secrets/peloton_api_auth.json") as file:
            return json.load(file)

    def _create_authenticated_api_session(self):
        auth_config = self.load_auth_config()
        payload = {
            "username_or_email": auth_config["username"],
            "password": auth_config["password"],
            "with_pubsub": False,
        }

        self.api_session = requests.Session()
        response = self.api_session.post(
            self._generate_full_uri(self.AUTH_LOGIN_ENDPOINT),
            json=payload,
            headers=self.headers,
            auth=HTTPBasicAuth(payload["username_or_email"], payload["password"]),
        )
        self._handle_bad_response(response)

        self.authorized_user_id = response.json()["user_id"]

    def request(self, endpoint: str, **parameters):
        response = self.api_session.get(
            self._generate_full_uri(endpoint), headers=self.headers, params=parameters
        )
        self._handle_bad_response(response)
        return response

    def fetch_all(self, endpoint: str, **params):
        params = {
            **params,
            "page": 0,
            "limit": 100,
            "joins": "ride,ride.instructor",
        }
        full_response = []
        response = self.request(endpoint, **params).json()

        data = response["data"]
        full_response.extend(data)

        for i in range(1, response["page_count"]):
            params["page"] += 1
            response = self.request(endpoint, **params).json()
            data = response["data"]
            full_response.extend(data)

        return full_response

    @staticmethod
    def _handle_bad_response(response):
        response.raise_for_status()
        if 300 <= response.status_code < 400:
            raise Exception("Unexpected redirect.")
