from dataclasses import dataclass
from os import getenv
from typing import Optional

import inject
from sqlalchemy import URL, Engine, create_engine

from peloton_metrics.helpers.secret_manager import SecretManager


@dataclass
class Settings:
    postgresDBEngine: Engine



def production() -> Settings:
    # TODO: Fill this out once there is a prod environment.
    raise NotImplementedError("Production Environment Not Yet Implemented")

def development() -> Settings:
    # TODO: Fill this out once there is a dev environment.
    raise NotImplementedError("Development Environment Not Yet Implemented")


def local() -> Settings:
    secret_manager = SecretManager()
    postgresDBEngine = create_engine(
        URL.create(
            "postgresql+psycopg",
            username=secret_manager.fetch_psql_username(),
            password=secret_manager.fetch_psql_password(),
            host="postgres",
            port="5432",
            database="peloton_metrics"
        )
    )
    def inject_config(binder):
        binder.bind(
            Engine,
            postgresDBEngine
        )
    inject.configure_once(inject_config)

    return Settings(
        postgresDBEngine=postgresDBEngine
    )
    

def testing():
    # TODO: Fill this out once there is a testing environment.
    raise NotImplementedError("Testing Environment Not Yet Implemented")

AVAILABLE_ENVIRONMENTS = {
     "local": local,
    #  "production": production,
    #  "development": development,
    #  "testing": testing
}


settings: Optional[Settings] = None
def get_settings() -> Settings:
    global settings
    if settings is not None:
         return settings

    current_environment = getenv("RUNTIME_ENVIRONMENT")
    if current_environment is None or current_environment not in AVAILABLE_ENVIRONMENTS:
            raise ValueError(f"Unsupported Environment '{current_environment}'. Available environments are: {Settings.AVAILABLE_ENVIRONMENTS}")

    settings = AVAILABLE_ENVIRONMENTS[current_environment]()
    return settings