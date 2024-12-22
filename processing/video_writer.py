from abc import ABC, abstractmethod


class VideoWriter(ABC):
    @abstractmethod
    def write(self, frame):
        pass

    @abstractmethod
    def release(self):
        pass
