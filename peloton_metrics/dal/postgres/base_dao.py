import inject
from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import text


class BaseDao:

    @inject.autoparams("psqlEngine")
    def __init__(self, psqlEngine: Engine):
        self.engine = psqlEngine
        self.connection = self.engine.connect()
        self.session: Session = sessionmaker(self.engine)

    def execute_sql(self, sql: str, params: dict = {}) -> list[dict]:
        return self.connection.execute(text(sql), parameters=params).fetchall()
