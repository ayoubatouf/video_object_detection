from audio.audio_extractor import AudioExtractor
import subprocess


class FFmpegAudioExtractor(AudioExtractor):
    def extract(self, input_video_path):
        audio_extraction_command = [
            "ffmpeg",
            "-i",
            input_video_path,
            "-q:a",
            "0",
            "-map",
            "a",
            "extracted_audio.mp3",
            "-y",
        ]
        try:
            subprocess.run(audio_extraction_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error during audio extraction: {e}")
            raise
