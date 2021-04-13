"""
The main Peloton API client.

@author Brad Snay <bradsnay@gmail.com>
"""
import requests


class PelotonApiClient:

    BASE_URL = 'https://api.onepeloton.com'
    USER_AGENT = "https://github.com/snayski/peloton_metrics"

    AUTH_LOGIN_URI = '/auth/login'

    # Headers we'll be using for each request
    headers = {
        "Content-Type": "application/json",
        "User-Agent": USER_AGENT
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

    def _generate_full_uri(self, endpoint: str):
        return f"{self.BASE_URL}{endpoint}",

    @staticmethod
    def _handle_bad_response(response):
        response.raise_for_status()

        if 300 <= response.status_code < 400:
            raise Exception("Unexpected redirect.")

    def _create_authenticated_api_session(self):
        payload = {
            'username_or_email': self.user_name,
            'password': self.password
        }

        self.api_session = requests.Session()

        response = self.api_session.post(
            self._generate_full_uri(self.AUTH_LOGIN_URI), json=payload, headers=self.headers)
        self._handle_bad_response(response)

        self.user_id = response.json()['user_id']

    def request(self, endpoint: str, **parameters):
        if not self.api_session:
            self._create_authenticated_api_session()

        response = self.api_session.get(self._generate_full_uri(endpoint), headers=self.headers, params=parameters)
        self._handle_bad_response(response)

        return response
