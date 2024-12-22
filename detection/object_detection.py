from ultralytics import YOLO
from audio.ffmpeg_audio_extractor import FFmpegAudioExtractor
from processing.ffmpeg_video_audio_merger import FFmpegVideoAudioMerger
from processing.opencv_video_source import OpenCVVideoSource
from processing.opencv_video_writer import OpenCVVideoWriter
from input_output.report import Report
from processing.video_processor import VideoProcessor
from detection.yolo_frame_processor import YOLOFrameProcessor
import os


def detect_objects(input_video_path, output_video_path, report_output_path):
    processed_video_path = "processed_video_no_audio.mp4"

    report = Report(report_output_path)

    video_source = OpenCVVideoSource(input_video_path)
    video_source.open()

    frame_width, frame_height, fps, total_frames = video_source.get_properties()

    model = YOLO("yolo11m.pt")
    frame_processor = YOLOFrameProcessor(model, model.names)
    video_writer = OpenCVVideoWriter(
        processed_video_path, frame_width, frame_height, fps
    )

    audio_extractor = FFmpegAudioExtractor()
    video_audio_merger = FFmpegVideoAudioMerger()

    final_output_path = output_video_path

    video_processor = VideoProcessor(
        video_source,
        frame_processor,
        video_writer,
        audio_extractor,
        video_audio_merger,
        report,
        processed_video_path,
        final_output_path,
    )

    video_processor.process()
    video_processor.extract_and_merge_audio()

    os.remove(processed_video_path)
    os.remove("extracted_audio.mp3")

    print(f"Final video with audio saved as '{output_video_path}'")
