"""
Static test for api client for snayski

@author Brad Snay <bradsnay@gmail.com>
"""
from peloton_metrics.dal.peloton_api_clients.workout_metrics_client import WorkoutMetricsClient
from peloton_metrics.dal.peloton_api_clients.user_client import UserClient
from peloton_metrics.processors.workout_metrics_follower_crawler import WorkoutMetricsFollowerCrawler
from peloton_metrics.processors.refresh_workout_processor import RefreshWorkoutProcessor
from peloton_metrics.metrics_extraction.workout_performance_extractor import WorkoutPerformanceExtractor

# scraper = WorkoutMetricsFollowerCrawler()
# scraper.run('1e160745a4af46debe245ae18d6e309c', depth=2)

RefreshWorkoutProcessor().run()

# client = WorkoutMetricsClient()
# performance_metrics = client.fetch_workout_performance_metrics('6c5e496bf5c041b9bfa0fba35bec211b')
# metrics = WorkoutPerformanceExtractor.extract_all_performance_metrics(
#     '6c5e496bf5c041b9bfa0fba35bec211b',
#     performance_metrics
# )
# print(metrics)

