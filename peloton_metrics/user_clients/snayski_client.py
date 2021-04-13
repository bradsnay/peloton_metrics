"""
Snayski user client.

@author Brad Snay <bradsnay@gmail.com>
"""
from peloton_metrics.user_clients.base_user_client import BaseUserClient


class SnayskiClient(BaseUserClient):
    def get_user_name(self) -> str:
        return "snayski"
