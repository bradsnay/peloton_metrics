from typing import List

from sqlalchemy import text
from sqlalchemy.orm import Session

from peloton_metrics.dal.helpers.decorators import select_as_models
from peloton_metrics.dal.helpers.sql_json_helper import SqlJsonHelper
from peloton_metrics.dal.helpers.sql_type_constants import SqlType
from peloton_metrics.dal.postgres.base_dao import BaseDao
from peloton_metrics.models.user import User


class TrackedUsersDao(BaseDao):

    @select_as_models(User)
    def fetch_tracked_users(self) -> List[User]:
        sql = f"""
            SELECT
                user_id AS user_id
                ,date_initialized AS date_initialized
                ,last_updated AS last_updated
                ,username AS username
                ,location AS location
                ,image_url AS image_url
                ,total_workouts AS total_workouts
                ,peloton_join_date AS peloton_join_date
            FROM public.tracked_users;
        """
        return self.execute_sql(sql)

    def upsert_tracked_user(self, user: User):
        column_map = {
            "user_id": SqlType.TEXT,
            "username": SqlType.TEXT,
            "location": SqlType.TEXT,
            "image_url": SqlType.TEXT,
            "total_workouts": SqlType.INT,
            "peloton_join_date": SqlType.TIMESTAMP,
        }
        with self.session() as session:
            SqlJsonHelper.populate_temp_table_from_model_sql(
                user, column_map, "NewUser", session
            )
            sql = f"""
                MERGE INTO public.tracked_users target
                USING NewUser source ON source.user_id = target.user_id
                WHEN MATCHED THEN
                    UPDATE SET
                        last_updated = NOW(),
                        username = source.username,
                        location = source.location,
                        image_url = source.image_url,
                        total_workouts = source.total_workouts,
                        peloton_join_date = source.peloton_join_date
                WHEN NOT MATCHED THEN
                INSERT (
                    user_id
                    ,last_updated
                    ,username
                    ,location
                    ,image_url
                    ,total_workouts
                    ,peloton_join_date
                )
            VALUES(
                    source.user_id
                    , NOW()
                    ,source.username
                    ,source.location
                    ,source.image_url
                    ,source.total_workouts
                    ,source.peloton_join_date
                );
            """
            session.execute(text(sql))
            session.commit()
