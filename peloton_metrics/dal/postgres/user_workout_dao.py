from peloton_metrics.dal.postgres.base_dao import BaseDao

class WorkoutDao(BaseDao):

    def save_all_workout_data(self, rows_to_save: list):
        pass

    def fetch_most_recently_saved_workout_timestamp(self, user_id: str):
        pass
        # job_config = bigquery.QueryJobConfig(
        #     query_parameters=[
        #         bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
        #     ]
        # )
        # sql = f"""
        #     SELECT
        #         created_at
        #     FROM `pelotonmetrics.peloton_metrics.user_workouts`
        #     WHERE user_id = @user_id
        #     ORDER BY created_at DESC
        #     LIMIT 1;
        # """
        # query_job = self.client.query(sql, job_config=job_config)
        # rows = query_job.result()
        # for row in rows:
        #     return int(row["created_at"])
        # # We haven't saved anything for this user yet.
        # return 0
