from google.cloud import bigquery


class TrackedUsersDao:

    def __init__(self):
        self.client = bigquery.Client()

    def fetch_tracked_users(self):
        sql = f"""
            SELECT user_id FROM `pelotonmetrics.peloton_metrics.tracked_users`
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
