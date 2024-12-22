from audio.video_audio_merger import VideoAudioMerger
import subprocess


class FFmpegVideoAudioMerger(VideoAudioMerger):
    def merge(self, video_path, audio_path, output_path):
        merge_command = [
            "ffmpeg",
            "-i",
            video_path,
            "-i",
            audio_path,
            "-c:v",
            "libx264",
            "-crf",
            "23",
            "-preset",
            "fast",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            output_path,
            "-y",
        ]
        try:
            subprocess.run(merge_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error during video and audio merge: {e}")
            raise
