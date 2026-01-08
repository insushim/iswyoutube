"""Shorts Converter - Convert long-form videos to Shorts"""
from typing import Dict, List
from pathlib import Path

class ShortsConverter:
    def __init__(self, config: Dict):
        self.config = config
        self.shorts_config = config.get('shorts', {})

    async def convert(self, video_path: str, start: float, duration: float, output_path: str = None) -> str:
        try:
            from moviepy.editor import VideoFileClip
            if not output_path:
                output_path = video_path.replace(".mp4", "_short.mp4")
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            video = VideoFileClip(video_path).subclip(start, start + min(duration, 60))
            w, h = video.size
            new_w = int(h * 9 / 16)
            video = video.crop(x1=(w - new_w) // 2, x2=(w + new_w) // 2).resize((1080, 1920))
            video.write_videofile(output_path, fps=30, codec='libx264')
            video.close()
            return output_path
        except Exception as e:
            raise RuntimeError(f"Shorts conversion failed: {e}")

    async def batch_convert(self, video_path: str, segments: List[Dict], output_dir: str) -> List[str]:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        results = []
        for i, seg in enumerate(segments[:self.shorts_config.get('generation', {}).get('count_per_video', 3)]):
            output = str(Path(output_dir) / f"short_{i:02d}.mp4")
            try:
                result = await self.convert(video_path, seg.get('start', 0), seg.get('duration', 30), output)
                results.append(result)
            except: pass
        return results
