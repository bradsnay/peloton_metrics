import json
from typing import List

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from peloton_metrics.dal.helpers.sql_type_constants import SqlType


class SqlJsonHelper:

    @staticmethod
    def populate_temp_table_from_model_sql(
        model: BaseModel,
        column_map: dict[str, SqlType],
        table_name: str,
        session: Session,
    ) -> None:
        column_names = ",".join([column_name for column_name in column_map.keys()])
        column_schema = ",".join(
            [
                f"{column_name} {column_type}"
                for column_name, column_type in column_map.items()
            ]
        )
        session.execute(
            text(
                f"""
                DROP TABLE IF EXISTS {table_name};
                """
            )
        )
        session.execute(
            text(
                f"""
                CREATE TEMP TABLE {table_name} (
                    {column_schema}
                );
            """
            )
        )
        session.execute(
            text(
                f"""
                INSERT INTO {table_name}(
                    {column_names}
                )
                SELECT
                    {column_names}
                FROM json_populate_record(null::{table_name}, :json);
                """
            ),
            {"json": model.model_dump_json()},
        )

    @staticmethod
    def populate_temp_table_from_model_list_sql(
        models: List[BaseModel],
        column_map: dict[str, SqlType],
        table_name: str,
        session: Session,
    ) -> None:
        column_names = ",".join([column_name for column_name in column_map.keys()])
        column_schema = ",".join(
            [
                f"{column_name} {column_type}"
                for column_name, column_type in column_map.items()
            ]
        )
        session.execute(
            text(
                f"""
                DROP TABLE IF EXISTS {table_name};
                """
            )
        )
        session.execute(
            text(
                f"""
                CREATE TEMP TABLE {table_name} (
                    {column_schema}
                );
            """
            )
        )
        session.execute(
            text(
                f"""
                INSERT INTO {table_name}(
                    {column_names}
                )
                SELECT
                    {column_names}
                FROM json_populate_recordset(null::{table_name}, :json);
                """
            ),
            {"json": json.dumps([model.model_dump() for model in models])},
        )
