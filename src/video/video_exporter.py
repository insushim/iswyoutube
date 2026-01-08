"""Video Exporter Module - Export videos in various formats"""
from typing import Dict
from pathlib import Path

class VideoExporter:
    PRESETS = {
        "youtube": {"resolution": "1920x1080", "fps": 30, "bitrate": "8M"},
        "shorts": {"resolution": "1080x1920", "fps": 30, "bitrate": "4M"},
        "tiktok": {"resolution": "1080x1920", "fps": 30, "bitrate": "4M"},
    }
    def __init__(self, config: Dict): self.config = config

    async def export(self, video_path: str, preset: str = "youtube", output_path: str = None) -> str:
        try:
            from moviepy.editor import VideoFileClip
            settings = self.PRESETS.get(preset, self.PRESETS["youtube"])
            if not output_path:
                output_path = video_path.replace(".mp4", f"_{preset}.mp4")
            video = VideoFileClip(video_path)
            video.write_videofile(output_path, fps=settings["fps"], bitrate=settings["bitrate"])
            video.close()
            return output_path
        except Exception as e:
            return video_path
