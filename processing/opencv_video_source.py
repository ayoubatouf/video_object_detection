import cv2
from processing.video_source import VideoSource


class OpenCVVideoSource(VideoSource):
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.video_source = cv2.VideoCapture(self.video_path)
        if not self.video_source.isOpened():
            raise ValueError("Error: Unable to open video source!")

    def open(self):
        if not self.video_source.isOpened():
            raise ValueError("Error: Unable to open video source!")

    def read_frame(self):
        ret, frame = self.video_source.read()
        return ret, frame

    def get_properties(self):
        frame_width = int(self.video_source.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.video_source.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(self.video_source.get(cv2.CAP_PROP_FPS))
        total_frames = int(self.video_source.get(cv2.CAP_PROP_FRAME_COUNT))

        if frame_width == 0 or frame_height == 0 or fps == 0 or total_frames == 0:
            raise ValueError("Error: Video properties could not be determined!")

        return frame_width, frame_height, fps, total_frames

    def release(self):
        self.video_source.release()
