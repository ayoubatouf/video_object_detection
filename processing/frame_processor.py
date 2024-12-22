from abc import ABC, abstractmethod


class FrameProcessor(ABC):
    @abstractmethod
    def process(self, frame):
        pass
