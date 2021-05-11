from google.cloud import bigquery


class TrackedUsersDao:
    def __init__(self):
        self.client = bigquery.Client()

    def fetch_tracked_users(self):
        sql = f"""
            SELECT user_id FROM `pelotonmetrics.peloton_metrics.tracked_users`;
        """
        return self.client.query(sql).result()

    def update_tracked_users(self):
        sql = f"""
            INSERT INTO `pelotonmetrics.peloton_metrics.tracked_users` (
                user_id,
                username
            )
            SELECT DISTINCT
                i.user_id,
                i.user_name
            FROM `pelotonmetrics.peloton_metrics.user_workouts` i
            LEFT JOIN `pelotonmetrics.peloton_metrics.tracked_users` u on i.user_id = u.user_id
            WHERE u.user_id IS NULL;
        """
        query_job = self.client.query(sql)
        result = query_job.result()

        return result

    def insert_new_tracked_user(self, user_id: str, user_name: str):
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("user_id", "STRING", user_id),
                bigquery.ScalarQueryParameter("user_name", "STRING", user_name),
            ]
        )
        sql = f"""
            INSERT INTO `pelotonmetrics.peloton_metrics.tracked_users` (
                user_id,
                username
            )
            SELECT
                i.user_id,
                i.user_name
            FROM (
                SELECT
                    @user_id AS user_id,
                    @user_name AS user_name
            ) i
            LEFT JOIN `pelotonmetrics.peloton_metrics.tracked_users` t on t.user_id = i.user_id
            WHERE t.user_id IS NULL;
        """
        query_job = self.client.query(sql, job_config=job_config)
        result = query_job.result()

        return result
