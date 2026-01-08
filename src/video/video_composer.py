"""Video Composer Module - Compose final video from components"""
from typing import Dict, List
from pathlib import Path

class VideoComposer:
    def __init__(self, config: Dict):
        self.config = config
        self.video_config = config.get('video', {})

    async def compose(self, images: List[str], audio_path: str, output_path: str, duration: float = None) -> str:
        try:
            from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            audio = AudioFileClip(audio_path) if Path(audio_path).exists() else None
            total_duration = audio.duration if audio else duration or 60
            clips = []
            clip_duration = total_duration / max(len(images), 1)
            for img_path in images:
                if Path(img_path).exists():
                    clip = ImageClip(img_path).set_duration(clip_duration).resize((1920, 1080))
                    clip = clip.crossfadein(0.5).crossfadeout(0.5)
                    clips.append(clip)
            if clips:
                video = concatenate_videoclips(clips, method='compose')
                if audio:
                    video = video.set_audio(audio)
                video.write_videofile(output_path, fps=self.video_config.get('fps', 30), codec='libx264')
                video.close()
                if audio: audio.close()
            return output_path
        except Exception as e:
            raise RuntimeError(f"Video composition failed: {e}")
