from datetime import datetime

from sqlalchemy import text

from peloton_metrics.dal.helpers.sql_json_helper import SqlJsonHelper
from peloton_metrics.dal.helpers.sql_type_constants import SqlType
from peloton_metrics.dal.postgres.base_dao import BaseDao
from peloton_metrics.models.workout import Workout
from peloton_metrics.models.workout_performance_metrics import WorkoutPerformanceMetrics


class WorkoutDao(BaseDao):

    def fetch_saved_workout_count(self, user_id: str) -> int:
        sql = """
            SELECT
                COUNT(1) as workout_count
            FROM public.workouts
            WHERE user_id = :user_id;
        """
        res = self.execute_sql(sql, {"user_id": user_id})
        if len(res) == 0:
            return 0
        return res[0]._asdict()["workout_count"]

    def save_all_workout_data(
        self,
        workouts_to_save: list[Workout],
        performance_metrics_to_save: list[WorkoutPerformanceMetrics],
    ):
        with self.session() as session:
            workout_column_map = {
                "workout_id": SqlType.TEXT,
                "user_id": SqlType.TEXT,
                "created_at": SqlType.TIMESTAMP,
                "start_time": SqlType.TIMESTAMP,
                "end_time": SqlType.TIMESTAMP,
                "timezone": SqlType.TEXT,
                "status": SqlType.TEXT,
                "device_type": SqlType.TEXT,
                "fitness_discipline": SqlType.TEXT,
                "has_pedaling_metrics": SqlType.BOOLEAN,
                "has_leaderboard_metrics": SqlType.BOOLEAN,
                "total_work": SqlType.REAL,
                "is_total_work_personal_record": SqlType.BOOLEAN,
                "is_outdoor": SqlType.BOOLEAN,
                "metrics_type": SqlType.TEXT,
                "name": SqlType.TEXT,
                "peloton_id": SqlType.TEXT,
                "platform": SqlType.TEXT,
                "workout_type": SqlType.TEXT,
                "total_watch_time_seconds": SqlType.INT,
                "difficulty_rating_avg": SqlType.REAL,
                "difficulty_rating_count": SqlType.INT,
                "difficulty_level": SqlType.TEXT,
                "duration": SqlType.INT,
                "image_url": SqlType.TEXT,
                "title": SqlType.TEXT,
                "instructor_id": SqlType.TEXT,
                "instructor_first_name": SqlType.TEXT,
                "instructor_last_name": SqlType.TEXT,
            }
            metrics_column_map = {
                "workout_id": SqlType.TEXT,
                "duration": SqlType.INT,
                "total_output": SqlType.INT,
                "output_unit": SqlType.TEXT,
                "total_distance": SqlType.REAL,
                "distance_unit": SqlType.TEXT,
                "total_calories": SqlType.INT,
                "calories_unit": SqlType.TEXT,
                "avg_output": SqlType.INT,
                "avg_cadence": SqlType.INT,
                "max_cadence": SqlType.INT,
                "cadence_unit": SqlType.TEXT,
                "avg_resistance": SqlType.INT,
                "max_resistance": SqlType.INT,
                "resistance_unit": SqlType.TEXT,
                "avg_speed": SqlType.REAL,
                "max_speed": SqlType.REAL,
                "speed_unit": SqlType.TEXT,
            }
            SqlJsonHelper.populate_temp_table_from_model_list_sql(
                workouts_to_save, workout_column_map, "WorkoutsToSave", session
            )
            SqlJsonHelper.populate_temp_table_from_model_list_sql(
                performance_metrics_to_save,
                metrics_column_map,
                "MetricsToSave",
                session,
            )

            sql = """
                INSERT INTO public.workouts(
                    workout_id
                    ,user_id
                    ,created_at
                    ,start_time
                    ,end_time
                    ,timezone
                    ,status
                    ,device_type
                    ,fitness_discipline
                    ,has_pedaling_metrics
                    ,has_leaderboard_metrics
                    ,total_work
                    ,is_total_work_personal_record
                    ,is_outdoor
                    ,metrics_type
                    ,name
                    ,peloton_id
                    ,platform
                    ,workout_type
                    ,total_watch_time_seconds
                    ,difficulty_rating_avg
                    ,difficulty_rating_count
                    ,difficulty_level
                    ,duration
                    ,image_url
                    ,title
                    ,instructor_id
                    ,instructor_first_name
                    ,instructor_last_name
                )
                SELECT
                    s.workout_id
                    ,s.user_id
                    ,s.created_at
                    ,s.start_time
                    ,s.end_time
                    ,s.timezone
                    ,s.status
                    ,s.device_type
                    ,s.fitness_discipline
                    ,s.has_pedaling_metrics
                    ,s.has_leaderboard_metrics
                    ,s.total_work
                    ,s.is_total_work_personal_record
                    ,s.is_outdoor
                    ,s.metrics_type
                    ,s.name
                    ,s.peloton_id
                    ,s.platform
                    ,s.workout_type
                    ,s.total_watch_time_seconds
                    ,s.difficulty_rating_avg
                    ,s.difficulty_rating_count
                    ,s.difficulty_level
                    ,s.duration
                    ,s.image_url
                    ,s.title
                    ,s.instructor_id
                    ,s.instructor_first_name
                    ,s.instructor_last_name
                FROM WorkoutsToSave s;
            """
            session.execute(text(sql))

            sql = """
                INSERT INTO public.workout_performance_metrics(
                    workout_id
                    ,duration
                    ,total_output
                    ,output_unit
                    ,total_distance
                    ,distance_unit
                    ,total_calories
                    ,calories_unit
                    ,avg_output
                    ,avg_cadence
                    ,max_cadence
                    ,cadence_unit
                    ,avg_resistance
                    ,max_resistance
                    ,resistance_unit
                    ,avg_speed
                    ,max_speed
                    ,speed_unit
                )
                SELECT
                    s.workout_id
                    ,s.duration
                    ,s.total_output
                    ,s.output_unit
                    ,s.total_distance
                    ,s.distance_unit
                    ,s.total_calories
                    ,s.calories_unit
                    ,s.avg_output
                    ,s.avg_cadence
                    ,s.max_cadence
                    ,s.cadence_unit
                    ,s.avg_resistance
                    ,s.max_resistance
                    ,s.resistance_unit
                    ,s.avg_speed
                    ,s.max_speed
                    ,s.speed_unit
                FROM MetricsToSave s;
            """
            session.execute(text(sql))
            session.commit()

    def fetch_most_recently_saved_workout_timestamp(self, user_id: str):
        sql = f"""
            SELECT
                created_at as created_at
            FROM public.workouts
            WHERE user_id = :user_id
            ORDER BY created_at DESC
            LIMIT 1;
        """
        result = self.execute_sql(sql, {"user_id": user_id})
        if len(result) == 0:
            # We haven't saved anything for this user yet.
            return 0

        return result[0]._asdict()["created_at"].timestamp()
