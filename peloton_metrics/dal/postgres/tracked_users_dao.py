from peloton_metrics.dal.postgres.base_dao import BaseDao


class TrackedUsersDao(BaseDao):

    def fetch_tracked_users(self):
        sql = f"""
            SELECT user_id FROM public.tracked_users;
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

    def insert_new_tracked_user(self, user_id: str, user_name: str):
        # TODO: Try to refactor this into a MERGE statement 
        sql = f"""
            INSERT INTO public.tracked_users (
                user_id,
                username
            )
            SELECT
                i.user_id,
                i.user_name
            FROM (
                SELECT
                    :user_id AS user_id,
                    :user_name AS user_name
            ) i
            LEFT JOIN public.tracked_users t on t.user_id = i.user_id
            WHERE t.user_id IS NULL;
        """
        return self.execute_sql(sql, {"user_id": user_id, "user_name": user_name})
