from peloton_metrics.models.workout_performance_metrics import WorkoutPerformanceMetrics


class WorkoutPerformanceExtractor:
    @staticmethod
    def extract_all_performance_metrics(
        workout_metrics: dict, workout_id: str
    ) -> WorkoutPerformanceMetrics:
        return WorkoutPerformanceMetrics(
            **{
                "workout_id": workout_id,
                **WorkoutPerformanceExtractor.fetch_duration(workout_metrics),
                **WorkoutPerformanceExtractor.fetch_summaries(workout_metrics),
                **WorkoutPerformanceExtractor.fetch_metrics(workout_metrics),
            }
        )

    @staticmethod
    def fetch_duration(workout_metrics: dict) -> dict:
        return {"duration": workout_metrics["duration"]}

    @staticmethod
    def fetch_summaries(workout_metrics: dict) -> dict:
        summaries = workout_metrics["summaries"]
        summaries_output = {}
        for val in summaries:
            slug = val["slug"]
            value = val["value"]
            display_unit = val["display_unit"]
            if slug == "total_output":
                summaries_output["total_output"] = value
                summaries_output["output_unit"] = display_unit
            if slug == "distance":
                summaries_output["total_distance"] = value
                summaries_output["distance_unit"] = display_unit
            if slug == "calories":
                summaries_output["total_calories"] = value
                summaries_output["calories_unit"] = display_unit
        return summaries_output

    @staticmethod
    def fetch_metrics(workout_metrics: dict) -> dict:
        metrics = workout_metrics["metrics"]
        metrics_output = {}

        for metric in metrics:
            slug = metric["slug"]
            max_value = metric["max_value"]
            avg_value = metric["average_value"]
            display_unit = metric["display_unit"]
            if slug == "output":
                metrics_output["avg_output"] = avg_value
                metrics_output["max_output"] = max_value
                metrics_output["output_unit"] = display_unit
            if slug == "cadence":
                metrics_output["avg_cadence"] = avg_value
                metrics_output["max_cadence"] = max_value
                metrics_output["cadence_unit"] = display_unit
            if slug == "resistance":
                metrics_output["avg_resistance"] = avg_value
                metrics_output["max_resistance"] = max_value
                metrics_output["resistance_unit"] = display_unit
            if slug == "speed":
                metrics_output["avg_speed"] = avg_value
                metrics_output["max_speed"] = max_value
                metrics_output["speed_unit"] = display_unit
            if slug == "heart_rate":
                metrics_output["avg_heartrate"] = avg_value
                metrics_output["max_heartrate"] = max_value
                metrics_output["heartrate_unit"] = display_unit
        return metrics_output
