from abc import ABC, abstractmethod


class VideoSource(ABC):
    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def read_frame(self):
        pass

    @abstractmethod
    def get_properties(self):
        pass

    @abstractmethod
    def release(self):
        pass
