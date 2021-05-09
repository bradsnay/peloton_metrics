"""
Static test for api client for snayski

@author Brad Snay <bradsnay@gmail.com>
"""
from peloton_metrics.user_clients.snayski_client import SnayskiClient

client = SnayskiClient()
client.save_all_workouts(client.fetch_all_workouts())
