from abc import ABC, abstractmethod

from settings import get_settings


class BaseProcessor(ABC):

    def __init__(self):
        self.settings = get_settings()
    
    @abstractmethod
    def run(self) -> None:
        pass

    def start(self) -> None:
        #TODO: Implement telemetry, exception handling etc.
        self.run()