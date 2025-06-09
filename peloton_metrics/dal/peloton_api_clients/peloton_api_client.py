"""
The main Peloton API client.

@author Brad Snay <bradsnay@gmail.com>
"""

import json
from os import getenv
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util import Retry


class PelotonApiClient:

    MAX_FETCH_LIMIT = 100

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
        with open(f"{getenv('SECRETS_FOLDER')}peloton_api_auth") as file:
            return json.load(file)

    def _create_authenticated_api_session(self):
        auth_config = self.load_auth_config()
        payload = {
            "username_or_email": auth_config["username"],
            "password": auth_config["password"],
            "with_pubsub": False,
        }
        retries = Retry(
            total=5,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504, 524],
            allowed_methods={"GET"},
        )
        self.api_session = requests.Session()
        self.api_session.mount("https://", HTTPAdapter(max_retries=retries))
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

    def fetch_all(self, endpoint: str, num_records: int = MAX_FETCH_LIMIT):
        params = {
            "page": 0,
            "limit": min(self.MAX_FETCH_LIMIT, num_records),
            "joins": "ride,ride.instructor",
        }
        full_response = []
        records_fetched = 0
        response = self.request(endpoint, **params).json()

        data = response["data"]
        records_fetched += response["count"]
        full_response.extend(data)
        if records_fetched < 100:
            return full_response

        params["limit"] = 100
        while records_fetched < num_records:
            params["page"] += 1

            response = self.request(endpoint, **params).json()
            data = response["data"]
            if len(data) == 0:
                break
            # We're only allowed to fetch 100 records at a time and changing the limit for pagination
            # affects how the page param is used. So we will over-fetch and only pull up to the number of
            # records we need.
            for i in range(min(num_records - records_fetched, len(data))):
                full_response.append(data[i])
                records_fetched += 1
        return full_response

    @staticmethod
    def _handle_bad_response(response):
        response.raise_for_status()
        if 300 <= response.status_code < 400:
            raise Exception("Unexpected redirect.")
