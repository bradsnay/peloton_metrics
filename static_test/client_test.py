"""
Static test for api client for snayski

@author Brad Snay <bradsnay@gmail.com>
"""
from peloton_metrics.dal.peloton_api_clients.workout_metrics_client import WorkoutMetricsClient
from peloton_metrics.dal.peloton_api_clients.user_client import UserClient
from peloton_metrics.processors.workout_metrics_follower_crawler import WorkoutMetricsFollowerCrawler
from peloton_metrics.processors.refresh_workout_processor import RefreshWorkoutProcessor


# scraper = WorkoutMetricsFollowerCrawler()
# scraper.run('1e160745a4af46debe245ae18d6e309c', depth=2)

RefreshWorkoutProcessor().run()


