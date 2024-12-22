import psutil
import torch


class Report:
    def __init__(self, output_file):
        self.output_file = output_file
        self.stats = {
            "Frame Processing Stats": {
                "Frames Processed": 0,
                "Frames Skipped": 0,
                "Processing Time Per Frame (ms)": 0,
            },
            "Object Detection Stats": {
                "Number of Objects Detected": 0,
                "Object Classes Detected": "",
                "Detection Confidence > 0.5": 0,
            },
            "Video Properties": {
                "Frame Rate (FPS)": 0,
                "Resolution (Width x Height)": "",
                "Total Frames in Video": 0,
            },
            "Video Processing Stats": {
                "Total Video Length (s)": 0,
                "Frames Processed per Second": 0,
            },
            "Audio Extraction and Merging Stats": {
                "Audio Extraction Time (s)": 0,
                "Audio Merge Time (s)": 0,
            },
            "Performance Stats": {
                "CPU Usage (%)": 0,
                "GPU Usage (%)": 0,
                "Memory Usage (MB)": 0,
            },
        }

    def update_frame_processing(
        self, frames_processed, frames_skipped, processing_time_per_frame
    ):
        self.stats["Frame Processing Stats"]["Frames Processed"] = frames_processed
        self.stats["Frame Processing Stats"]["Frames Skipped"] = frames_skipped
        self.stats["Frame Processing Stats"]["Processing Time Per Frame (ms)"] = round(
            processing_time_per_frame, 2
        )

    def update_object_detection(
        self, num_objects, high_confidence_classes, confident_detections
    ):
        self.stats["Object Detection Stats"]["Number of Objects Detected"] = num_objects
        self.stats["Object Detection Stats"][
            "Detection Confidence > 0.5"
        ] = confident_detections

        if high_confidence_classes:
            object_classes_str = ", ".join(
                [
                    f"{obj_class}: {count}"
                    for obj_class, count in high_confidence_classes.items()
                ]
            )
            self.stats["Object Detection Stats"][
                "Object Classes Detected"
            ] = object_classes_str
        else:
            self.stats["Object Detection Stats"]["Object Classes Detected"] = "None"

    def update_video_properties(self, fps, resolution, total_frames):
        self.stats["Video Properties"]["Frame Rate (FPS)"] = fps
        self.stats["Video Properties"]["Resolution (Width x Height)"] = resolution
        self.stats["Video Properties"]["Total Frames in Video"] = total_frames

    def update_video_processing(self, total_video_length, frames_processed_per_second):
        self.stats["Video Processing Stats"]["Total Video Length (s)"] = round(
            total_video_length, 2
        )
        self.stats["Video Processing Stats"]["Frames Processed per Second"] = round(
            frames_processed_per_second, 2
        )

    def update_audio_extraction_and_merging(self, extraction_time, merge_time):
        self.stats["Audio Extraction and Merging Stats"][
            "Audio Extraction Time (s)"
        ] = round(extraction_time, 2)
        self.stats["Audio Extraction and Merging Stats"]["Audio Merge Time (s)"] = (
            round(merge_time, 2)
        )

    def update_performance_stats(self):
        self.stats["Performance Stats"]["CPU Usage (%)"] = round(
            psutil.cpu_percent(interval=1), 2
        )

        if torch.cuda.is_available():
            self.stats["Performance Stats"]["GPU Usage (%)"] = round(
                torch.cuda.memory_allocated() / torch.cuda.max_memory_allocated() * 100,
                2,
            )
        else:
            self.stats["Performance Stats"]["GPU Usage (%)"] = 0

        self.stats["Performance Stats"]["Memory Usage (MB)"] = round(
            psutil.virtual_memory().used / 1024 / 1024, 2
        )

    def save_report(self):
        with open(self.output_file, "w") as f:
            for category, data in self.stats.items():
                f.write(f"{category}:\n")
                for stat, value in data.items():
                    f.write(f"  {stat}: {value}\n")
                f.write("\n")
