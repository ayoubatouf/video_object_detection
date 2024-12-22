from abc import ABC, abstractmethod


class AudioExtractor(ABC):
    @abstractmethod
    def extract(self, input_video_path):
        pass
