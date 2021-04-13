"""
The main Peloton API client.

@author Brad Snay <bradsnay@gmail.com>
"""
import requests
from requests.auth import HTTPBasicAuth


class PelotonApiClient:

    BASE_URL = "https://api.onepeloton.com"
    USER_AGENT = "https://github.com/snayski/peloton_metrics"

    AUTH_LOGIN_URI = '/auth/login'

    # Headers we'll be using for each request
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": USER_AGENT,
    }

    def __init__(self, user_name: str, password: str):
        if user_name is None:
            raise ValueError("No Peloton user name was provided.")
        if password is None:
            raise ValueError("No Peloton password was provided.")

        self.user_name: str = user_name
        self.password: str = password
        self.api_session = None
        self.user_id = None
        self._create_authenticated_api_session()

    def _generate_full_uri(self, endpoint: str) -> str:
        return f"{self.BASE_URL}{endpoint}"

    @staticmethod
    def _handle_bad_response(response):
        response.raise_for_status()

        if 300 <= response.status_code < 400:
            raise Exception("Unexpected redirect.")

    def _create_authenticated_api_session(self):
        payload = {
            'username_or_email': self.user_name,
            'password': self.password,
            'with_pubsub': False,
        }

        self.api_session = requests.Session()

        response = self.api_session.post(
            self._generate_full_uri(self.AUTH_LOGIN_URI),
            json=payload,
            headers=self.headers,
            auth=HTTPBasicAuth(self.user_name, self.password)
        )
        self._handle_bad_response(response)

        self.user_id = response.json()['user_id']

    def request(self, endpoint: str, **parameters):
        response = self.api_session.get(self._generate_full_uri(endpoint), headers=self.headers, params=parameters)
        self._handle_bad_response(response)

        return response
