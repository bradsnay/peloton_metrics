from google.cloud import bigquery


class BigTableClient:

    def __init__(self):
        self.client = bigquery.Client()

    @staticmethod
    def included_metrics() -> set:
        return {
            'created_at',
            'device_type',
            'end_time',
            'fitness_discipline',
            'has_pedaling_metrics',
            'has_leaderboard_metrics',
            'id',
            'is_total_work_personal_record',
            'metrics_type',
            'name',
            'peloton_id',
            'platform',
            'start_time',
            'status',
            'timezone',
            'title',
            'total_work',
            'user_id',
            'workout_type',
            'total_video_watch_time_seconds',
            'total_video_buffering_seconds',
            'v2_total_video_watch_time_seconds',
            'v2_total_video_buffering_seconds',
            'total_music_audio_play_seconds',
            'total_music_audio_buffer_seconds',
            'ride__difficulty_rating_avg',
            'ride__duration',
            'ride__fitness_discipline_display_name',
            'ride__id',
            'ride__image_url',
            'ride__length',
            'ride__overall_rating_avg',
            'ride__title',
            'ride__difficulty_estimate',
            'ride__instructor__name',
            'ride__instructor__username',
            'ride__instructor__image_url',
            'created',
            'device_time_created_at',
            'effort_zones__total_effort_points',
            'effort_zones__heart_rate_zone_durations__heart_rate_z1_duration',
            'effort_zones__heart_rate_zone_durations__heart_rate_z2_duration',
            'effort_zones__heart_rate_zone_durations__heart_rate_z3_duration',
            'effort_zones__heart_rate_zone_durations__heart_rate_z4_duration',
            'effort_zones__heart_rate_zone_durations__heart_rate_z5_duration',
        }

    def save_all_workout_data(self, user_name: str, workout_data: list):
        rows_to_save = []
        for workout in workout_data:
            row = {'user_name': user_name}
            for column in self.included_metrics():
                row[column] = self._fetch_value(column, workout)
            rows_to_save.append(row)
        # TODO: Need to only pull the data that's not already stored in BigQuery.
        errors = self.client.insert_rows_json(
            'pelotonmetrics.peloton_metrics.user_peloton_metrics',
            rows_to_save,
        )
        if errors:
            raise Exception("Encountered errors while inserting rows: {}".format(errors))

    def _fetch_value(self, column_key: str, workout: dict):
        keys = column_key.split('__')
        return self._fetch_value_recursive(keys, workout)

    def _fetch_value_recursive(self, keys: list, workout: dict):
        if len(keys) == 0 or workout is None:
            return str(workout)
        if keys[0] in workout:
            return self._fetch_value_recursive(keys[1:], workout[keys[0]])

