from peloton_metrics.processors.base_processor import BaseProcessor
from peloton_metrics.dal.peloton_api_clients.user_client import UserClient

class UserInitializationProcessor(BaseProcessor):

    def __init__(self):
        super().__init__()
        self.user_client = UserClient()
    
    def run(self):
        identity = self.user_client.self_identify()
        print(identity)