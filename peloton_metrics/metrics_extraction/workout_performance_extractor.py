

class WorkoutPerformanceExtractor:
    @staticmethod
    def extract_all_performance_metrics(workout_metrics: dict) -> dict:
        return {
            **WorkoutPerformanceExtractor.fetch_duration(workout_metrics),
            **WorkoutPerformanceExtractor.fetch_summaries(workout_metrics),
            **WorkoutPerformanceExtractor.fetch_metrics(workout_metrics),
        }

    @staticmethod
    def fetch_duration(workout_metrics: dict) -> dict:
        return {'duration': workout_metrics['duration']}

    @staticmethod
    def fetch_summaries(workout_metrics: dict) -> dict:
        summaries = workout_metrics['summaries']
        summaries_output = {}
        for total in summaries:
            slug = total['slug']
            value = total['value']
            if slug == 'total_output':
                summaries_output['total_output'] = value
            if slug == 'distance':
                summaries_output['total_distance'] = value
            if slug == 'calories':
                summaries_output['total_calories'] = value
        return summaries_output

    @staticmethod
    def fetch_metrics(workout_metrics: dict) -> dict:
        metrics = workout_metrics['metrics']
        metrics_output = {}

        for metric in metrics:
            slug = metric['slug']
            max_value = metric['max_value']
            avg_value = metric['average_value']
            if slug == 'output':
                metrics_output['avg_output'] = avg_value
                metrics_output['max_output'] = max_value
            if slug == 'cadence':
                metrics_output['avg_cadence'] = avg_value
                metrics_output['max_cadence'] = max_value
            if slug == 'resistance':
                metrics_output['avg_resistance'] = avg_value
                metrics_output['max_resistance'] = max_value
            if slug == 'speed':
                metrics_output['avg_speed'] = avg_value
                metrics_output['max_speed'] = max_value
            if slug == 'heart_rate':
                metrics_output['avg_heartrate'] = avg_value
                metrics_output['max_heartrate'] = max_value
        return metrics_output
