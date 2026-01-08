"""
SFX Manager Module
==================
Manage sound effects for videos
"""

from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass
import random


@dataclass
class SoundEffect:
    """효과음"""
    path: str
    name: str
    category: str
    duration: float
    volume_level: float


class SFXManager:
    """효과음 관리자"""

    CATEGORIES = {
        "transition": "장면 전환",
        "emphasis": "강조",
        "notification": "알림",
        "whoosh": "휘파람 소리",
        "impact": "임팩트",
        "success": "성공",
        "error": "오류",
        "typing": "타이핑",
        "pop": "팝",
        "click": "클릭",
    }

    def __init__(self, config: Dict):
        self.config = config
        self.sfx_config = config.get('audio', {}).get('sfx', {})
        self.library_path = Path("assets/sound_effects")

    async def get_sfx(
        self,
        category: str,
        variant: int = None
    ) -> Optional[SoundEffect]:
        """
        효과음 가져오기

        Args:
            category: 카테고리
            variant: 변형 번호

        Returns:
            효과음
        """
        category_path = self.library_path / category
        if not category_path.exists():
            return None

        files = list(category_path.glob("*.mp3")) + list(category_path.glob("*.wav"))

        if not files:
            return None

        if variant is not None and variant < len(files):
            file_path = files[variant]
        else:
            file_path = random.choice(files)

        return SoundEffect(
            path=str(file_path),
            name=file_path.stem,
            category=category,
            duration=await self._get_duration(file_path),
            volume_level=self.sfx_config.get('volume', 0.3)
        )

    async def get_transition_sfx(self) -> Optional[SoundEffect]:
        """전환 효과음"""
        return await self.get_sfx("transition")

    async def get_emphasis_sfx(self) -> Optional[SoundEffect]:
        """강조 효과음"""
        return await self.get_sfx("emphasis")

    async def get_notification_sfx(self) -> Optional[SoundEffect]:
        """알림 효과음"""
        return await self.get_sfx("notification")

    async def _get_duration(self, file_path: Path) -> float:
        """오디오 길이"""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(str(file_path))
            return len(audio) / 1000
        except Exception:
            return 1.0

    def list_categories(self) -> Dict[str, str]:
        """카테고리 목록"""
        return self.CATEGORIES

    async def list_sfx_in_category(self, category: str) -> List[SoundEffect]:
        """카테고리 내 효과음 목록"""
        category_path = self.library_path / category
        if not category_path.exists():
            return []

        sfx_list = []
        for file_path in category_path.glob("*.*"):
            if file_path.suffix in [".mp3", ".wav"]:
                sfx_list.append(SoundEffect(
                    path=str(file_path),
                    name=file_path.stem,
                    category=category,
                    duration=await self._get_duration(file_path),
                    volume_level=self.sfx_config.get('volume', 0.3)
                ))

        return sfx_list

    async def auto_suggest_sfx(
        self,
        script_segments: List[Dict]
    ) -> List[Dict]:
        """스크립트 기반 효과음 자동 제안"""
        suggestions = []

        for i, segment in enumerate(script_segments):
            segment_type = segment.get('type', '')

            if segment_type == 'transition' or i > 0:
                sfx = await self.get_transition_sfx()
                if sfx:
                    suggestions.append({
                        "segment_index": i,
                        "sfx": sfx,
                        "position": "start"
                    })

        return suggestions
