from sqlalchemy import text
from sqlalchemy.orm import Session

from peloton_metrics.dal.postgres.base_dao import BaseDao
from peloton_metrics.dal.postgres.helpers.decorators import select_as_dictionaries
from peloton_metrics.dal.postgres.helpers.json_helper import JsonHelper
from peloton_metrics.dal.postgres.helpers.sql_type_constants import SqlType
from peloton_metrics.models.user import User


class TrackedUsersDao(BaseDao):

    @select_as_dictionaries
    def fetch_tracked_users(self):
        sql = f"""
            SELECT
                user_id AS user_id
            FROM public.tracked_users;
        """
        return self.execute_sql(sql)

    def update_tracked_users(self):
        sql = f"""
            INSERT INTO public.tracked_users (
                user_id,
                username
            )
            SELECT DISTINCT
                i.user_id,
                i.user_name
            FROM public.user_workouts i
            LEFT JOIN public.tracked_users u on i.user_id = u.user_id
            WHERE u.user_id IS NULL;
        """
        return self.execute_sql(sql)

    def upsert_tracked_user(self, user: User):
        column_map = {
            "user_id": SqlType.TEXT,
            "date_initialized": SqlType.TIMESTAMP,
            "last_updated": SqlType.TIMESTAMP,
            "username": SqlType.TEXT,
            "first_name": SqlType.TEXT,
            "last_name": SqlType.TEXT,
            "location": SqlType.TEXT,
            "image_url": SqlType.TEXT,
            "gender": SqlType.TEXT,
            "weight": SqlType.REAL,
            "weight_unit": SqlType.TEXT,
            "height": SqlType.REAL,
            "height_unit": SqlType.TEXT,
            "total_workouts": SqlType.INT,
            "peloton_join_date": SqlType.TIMESTAMP,
            "birthday": SqlType.TIMESTAMP,
        }
        with self.session() as session:
            JsonHelper.populate_temp_table_from_model_sql(
                user, column_map, "NewUser", session
            )
            sql = f"""
                MERGE INTO public.tracked_users target
                USING NewUser source ON source.user_id = target.user_id
                WHEN MATCHED THEN
                    UPDATE SET
                        last_updated = NOW(),
                        first_name = source.first_name,
                        last_name = source.last_name,
                        location = source.location,
                        image_url = source.image_url,
                        gender = source.gender,
                        weight = source.weight,
                        weight_unit = source.weight_unit,
                        height = source.height,
                        height_unit = source.height_unit,
                        total_workouts = source.total_workouts,
                        peloton_join_date = source.peloton_join_date,
                        birthday = source.birthday
                WHEN NOT MATCHED THEN
                INSERT (
                    user_id
                    ,last_updated
                    ,username
                    ,first_name
                    ,last_name
                    ,location
                    ,image_url
                    ,gender
                    ,weight
                    ,weight_unit
                    ,height
                    ,height_unit
                    ,total_workouts
                    ,peloton_join_date
                    ,birthday
                )
            VALUES(
                    source.user_id
                    , NOW()
                    ,source.username
                    ,source.first_name
                    ,source.last_name
                    ,source.location
                    ,source.image_url
                    ,source.gender
                    ,source.weight
                    ,source.weight_unit
                    ,source.height
                    ,source.height_unit
                    ,source.total_workouts
                    ,source.peloton_join_date
                    ,source.birthday
                );
            """
            session.execute(text(sql))
            session.commit()
