"""
Animation Engine Module
=======================
Create animations for video content
"""

from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Animation:
    """애니메이션 데이터"""
    path: str
    duration: float
    animation_type: str
    fps: int


class AnimationEngine:
    """애니메이션 엔진"""

    ANIMATION_TYPES = {
        "ken_burns": "줌/팬 효과",
        "parallax": "레이어 패럴랙스",
        "fade": "페이드 인/아웃",
        "slide": "슬라이드",
        "zoom": "줌 인/아웃",
        "rotate": "회전",
    }

    def __init__(self, config: Dict):
        self.config = config
        self.animation_config = config.get('visual', {}).get('animation', {})

    async def create_ken_burns(
        self,
        image_path: str,
        duration: float,
        zoom_ratio: float = 0.04,
        direction: str = "random",
        output_path: str = None
    ) -> Animation:
        """
        Ken Burns 효과 생성

        Args:
            image_path: 이미지 경로
            duration: 길이
            zoom_ratio: 줌 비율
            direction: 방향
            output_path: 출력 경로

        Returns:
            애니메이션
        """
        if not output_path:
            output_path = image_path.replace(".png", "_kb.mp4")

        try:
            from moviepy.editor import ImageClip

            clip = ImageClip(image_path)
            clip = clip.set_duration(duration)
            clip = clip.resize((1920, 1080))

            # Ken Burns 효과 적용
            clip = clip.resize(lambda t: 1 + zoom_ratio * t / duration)

            clip.write_videofile(
                output_path,
                fps=self.animation_config.get('fps', 30),
                codec='libx264'
            )

            clip.close()

            return Animation(
                path=output_path,
                duration=duration,
                animation_type="ken_burns",
                fps=30
            )
        except ImportError:
            raise RuntimeError("moviepy not installed")

    async def create_parallax(
        self,
        layers: List[str],
        duration: float,
        depth: float = 0.1,
        output_path: str = None
    ) -> Animation:
        """패럴랙스 효과 생성"""
        if not output_path:
            output_path = "output/animations/parallax.mp4"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        try:
            from moviepy.editor import ImageClip, CompositeVideoClip

            clips = []
            for i, layer_path in enumerate(layers):
                clip = ImageClip(layer_path)
                clip = clip.set_duration(duration)

                # 레이어별 다른 속도 적용
                speed = 1 + (i * depth)
                clip = clip.set_position(
                    lambda t, s=speed: (int(t * 10 * s), 0)
                )

                clips.append(clip)

            final = CompositeVideoClip(clips)
            final.write_videofile(output_path, fps=30)

            for clip in clips:
                clip.close()
            final.close()

            return Animation(
                path=output_path,
                duration=duration,
                animation_type="parallax",
                fps=30
            )
        except ImportError:
            raise RuntimeError("moviepy not installed")

    async def create_transition(
        self,
        clip1_path: str,
        clip2_path: str,
        transition_type: str = "crossfade",
        duration: float = 0.5,
        output_path: str = None
    ) -> str:
        """전환 효과 생성"""
        if not output_path:
            output_path = "output/animations/transition.mp4"

        try:
            from moviepy.editor import VideoFileClip, concatenate_videoclips

            clip1 = VideoFileClip(clip1_path)
            clip2 = VideoFileClip(clip2_path)

            if transition_type == "crossfade":
                clip1 = clip1.crossfadeout(duration)
                clip2 = clip2.crossfadein(duration)

            final = concatenate_videoclips([clip1, clip2], method='compose')
            final.write_videofile(output_path, fps=30)

            clip1.close()
            clip2.close()
            final.close()

            return output_path
        except ImportError:
            raise RuntimeError("moviepy not installed")

    def get_available_animations(self) -> Dict[str, str]:
        """사용 가능한 애니메이션 목록"""
        return self.ANIMATION_TYPES
