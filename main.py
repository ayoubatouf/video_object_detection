from detection.object_detection import detect_objects


if __name__ == "__main__":
    input_video_path = "input_output/input_video.avi"
    output_video_path = "input_output/output_video.mp4"
    report_output_path = "input_output/processing_report.txt"

    detect_objects(input_video_path, output_video_path, report_output_path)
