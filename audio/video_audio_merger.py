from abc import ABC, abstractmethod


class VideoAudioMerger(ABC):
    @abstractmethod
    def merge(self, video_path, audio_path, output_path):
        pass
