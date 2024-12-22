from cv2 import VideoWriter
import cv2


class OpenCVVideoWriter(VideoWriter):
    def __init__(self, output_path, frame_width, frame_height, fps):
        self.out = cv2.VideoWriter(
            output_path,
            cv2.VideoWriter_fourcc(*"MP4V"),
            fps,
            (frame_width, frame_height),
        )

    def write(self, frame):
        self.out.write(frame)

    def release(self):
        self.out.release()
