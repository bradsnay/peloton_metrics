from os import getenv


class SecretManager:

    def __init__(self):
        self.secrets_folder = getenv('SECRETS_FOLDER')

    def fetch_psql_username(self) -> str:
        with open(f"{self.secrets_folder}postgres_user", 'r') as f:
            return f.read()

    def fetch_psql_password(self) -> str:
        with open(f"{self.secrets_folder}postgres_pw", 'r') as f:
            return f.read()