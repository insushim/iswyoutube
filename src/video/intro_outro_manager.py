"""Intro/Outro Manager Module - Manage intro and outro segments"""
from typing import Dict, Optional
from pathlib import Path

class IntroOutroManager:
    def __init__(self, config: Dict):
        self.config = config
        self.intro_config = config.get('video', {}).get('intro', {})
        self.outro_config = config.get('video', {}).get('outro', {})

    async def get_intro(self, template: str = "default") -> Optional[str]:
        intro_path = Path(f"assets/videos/intros/{template}.mp4")
        return str(intro_path) if intro_path.exists() else None

    async def get_outro(self, template: str = "subscribe_cta") -> Optional[str]:
        outro_path = Path(f"assets/videos/outros/{template}.mp4")
        return str(outro_path) if outro_path.exists() else None

    async def add_intro_outro(self, main_video: str, output_path: str) -> str:
        try:
            from moviepy.editor import VideoFileClip, concatenate_videoclips
            clips = []
            intro = await self.get_intro()
            if intro and self.intro_config.get('enabled'): clips.append(VideoFileClip(intro))
            clips.append(VideoFileClip(main_video))
            outro = await self.get_outro()
            if outro and self.outro_config.get('enabled'): clips.append(VideoFileClip(outro))
            if len(clips) > 1:
                final = concatenate_videoclips(clips)
                final.write_videofile(output_path, fps=30)
                final.close()
                for c in clips: c.close()
                return output_path
            return main_video
        except: return main_video
