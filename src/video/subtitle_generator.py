"""Subtitle Generator Module - Generate subtitles from script"""
from typing import Dict, List
from pathlib import Path

class SubtitleGenerator:
    def __init__(self, config: Dict):
        self.config = config
        self.subtitle_config = config.get('visual', {}).get('subtitle', {})

    async def generate_srt(self, script_segments: List[Dict], output_path: str) -> str:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        srt_content = []
        for i, segment in enumerate(script_segments, 1):
            start = segment.get('start_time', '00:00:00,000')
            end = segment.get('end_time', '00:00:30,000')
            text = segment.get('text', '')[:self.subtitle_config.get('max_chars_per_line', 40)]
            srt_content.append(f"{i}\n{start} --> {end}\n{text}\n")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(srt_content))
        return output_path

    async def burn_subtitles(self, video_path: str, srt_path: str, output_path: str) -> str:
        try:
            from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
            video = VideoFileClip(video_path)
            video.write_videofile(output_path, fps=30)
            video.close()
            return output_path
        except: return video_path
