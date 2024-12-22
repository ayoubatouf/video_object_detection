import time
from tqdm import tqdm


class VideoProcessor:
    def __init__(
        self,
        video_source,
        frame_processor,
        video_writer,
        audio_extractor,
        video_audio_merger,
        report,
        processed_video_path,
        final_output_path,
    ):
        self.video_source = video_source
        self.frame_processor = frame_processor
        self.video_writer = video_writer
        self.audio_extractor = audio_extractor
        self.video_audio_merger = video_audio_merger
        self.report = report
        self.processed_video_path = processed_video_path
        self.final_output_path = final_output_path

    def process(self):
        frame_idx = 0
        start_time = time.time()
        frames_skipped = 0
        total_objects = 0
        object_classes = set()
        confident_detections = 0
        all_high_confidence_classes = {}
        frame_width, frame_height, fps, total_frames = (
            self.video_source.get_properties()
        )
        resolution = f"{frame_width}x{frame_height}"
        self.report.update_video_properties(fps, resolution, total_frames)

        actual_video_length = total_frames / fps

        with tqdm(total=total_frames, desc="Processing Frames", unit="frame") as pbar:
            while True:
                ret, frame = self.video_source.read_frame()
                if not ret:
                    break
                frame_start_time = time.time()

                (
                    processed_frame,
                    num_objects,
                    high_confidence_classes,
                    confident_dets,
                ) = self.frame_processor.process(frame)
                self.video_writer.write(processed_frame)
                frame_end_time = time.time()

                total_objects += num_objects
                confident_detections += confident_dets

                for object_name, count in high_confidence_classes.items():
                    if object_name in all_high_confidence_classes:
                        all_high_confidence_classes[object_name] += count
                    else:
                        all_high_confidence_classes[object_name] = count

                frame_time = (frame_end_time - frame_start_time) * 1000

                self.report.update_frame_processing(
                    frame_idx + 1, frames_skipped, frame_time
                )

                self.report.update_object_detection(
                    total_objects, all_high_confidence_classes, confident_detections
                )

                frame_idx += 1

                pbar.update(1)

        end_time = time.time()
        total_video_length = end_time - start_time
        frames_per_second = frame_idx / total_video_length
        self.report.update_video_processing(total_video_length, frames_per_second)

        self.report.update_video_processing(actual_video_length, fps)

        self.video_source.release()
        self.video_writer.release()

    def extract_and_merge_audio(self):
        start_time = time.time()
        self.audio_extractor.extract(self.video_source.video_path)
        extraction_time = time.time() - start_time
        self.report.update_audio_extraction_and_merging(extraction_time, 0)

        start_time = time.time()
        self.video_audio_merger.merge(
            self.processed_video_path, "extracted_audio.mp3", self.final_output_path
        )
        merge_time = time.time() - start_time
        self.report.update_audio_extraction_and_merging(extraction_time, merge_time)

        self.report.update_performance_stats()

        self.report.save_report()
