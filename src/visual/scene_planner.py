"""
Scene Planner Module
====================
Plan visual scenes for video segments
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class Scene:
    """장면 데이터"""
    scene_id: int
    segment_id: int
    description: str
    visual_type: str  # image, animation, infographic, chart, map
    duration: float
    transition: str
    assets_needed: List[str]
    prompt: str


class ScenePlanner:
    """장면 기획기"""

    VISUAL_TYPES = {
        "hook": "image",
        "intro": "animation",
        "body": "infographic",
        "conclusion": "image",
        "cta": "animation",
    }

    def __init__(self, config: Dict):
        self.config = config

    async def plan_scenes(
        self,
        script_segments: List[Dict],
        style: str,
        total_duration: float
    ) -> List[Scene]:
        """
        장면 기획

        Args:
            script_segments: 스크립트 세그먼트
            style: 영상 스타일
            total_duration: 총 길이

        Returns:
            장면 리스트
        """
        scenes = []

        for i, segment in enumerate(script_segments):
            segment_type = segment.get('type', 'body')
            visual_note = segment.get('visual_note', '')
            duration = segment.get('duration', 30)

            # 비주얼 타입 결정
            visual_type = self.VISUAL_TYPES.get(segment_type, 'image')

            # 프롬프트 생성
            prompt = self._generate_prompt(
                visual_note or segment.get('text', '')[:100],
                style,
                visual_type
            )

            # 전환 효과 결정
            transition = self._get_transition(i, len(script_segments))

            scene = Scene(
                scene_id=i,
                segment_id=segment.get('id', i),
                description=visual_note,
                visual_type=visual_type,
                duration=duration,
                transition=transition,
                assets_needed=self._identify_assets(visual_note, visual_type),
                prompt=prompt
            )

            scenes.append(scene)

        return scenes

    def _generate_prompt(
        self,
        description: str,
        style: str,
        visual_type: str
    ) -> str:
        """이미지 생성 프롬프트 생성"""
        base_prompt = description

        style_additions = {
            "kurzgesagt": "flat design, pastel colors, minimal, geometric",
            "knowledge_pirate": "illustrated, warm colors, friendly",
            "veritasium": "realistic, scientific, documentary",
            "infographic": "data visualization, clean, modern",
        }

        type_additions = {
            "image": "detailed illustration",
            "infographic": "infographic layout, data visualization",
            "chart": "clean chart, data visualization",
            "map": "geographic illustration, map style",
        }

        additions = []
        if style in style_additions:
            additions.append(style_additions[style])
        if visual_type in type_additions:
            additions.append(type_additions[visual_type])

        additions.append("16:9 aspect ratio, high quality, no text")

        return f"{base_prompt}, {', '.join(additions)}"

    def _get_transition(self, index: int, total: int) -> str:
        """전환 효과 결정"""
        if index == 0:
            return "fade_in"
        elif index == total - 1:
            return "fade_out"
        else:
            return "crossfade"

    def _identify_assets(
        self,
        description: str,
        visual_type: str
    ) -> List[str]:
        """필요한 에셋 식별"""
        assets = []

        keywords = {
            "차트": "chart",
            "그래프": "chart",
            "지도": "map",
            "타임라인": "timeline",
            "아이콘": "icon",
            "로고": "logo",
        }

        for keyword, asset_type in keywords.items():
            if keyword in description:
                assets.append(asset_type)

        if not assets:
            assets.append(visual_type)

        return assets

    def optimize_scene_flow(self, scenes: List[Scene]) -> List[Scene]:
        """장면 흐름 최적화"""
        # 연속된 같은 타입 방지
        optimized = []
        for i, scene in enumerate(scenes):
            if i > 0 and scene.visual_type == scenes[i-1].visual_type:
                # 전환을 더 강조
                scene.transition = "wipe"
            optimized.append(scene)

        return optimized
