"""
BGM Selector Module
===================
Select appropriate background music
"""

from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass
import random


@dataclass
class BGMTrack:
    """BGM 트랙"""
    path: str
    name: str
    category: str
    mood: str
    duration: float
    tempo: str  # slow, medium, fast
    license: str


class BGMSelector:
    """BGM 선택기"""

    CATEGORY_MOODS = {
        "history": ["epic", "orchestral", "ambient", "dramatic"],
        "science": ["electronic", "ambient", "minimal", "curious"],
        "economy": ["corporate", "minimal", "upbeat", "serious"],
        "technology": ["electronic", "futuristic", "minimal", "innovative"],
        "philosophy": ["ambient", "contemplative", "minimal", "ethereal"],
        "culture": ["world", "ethnic", "acoustic", "warm"],
    }

    def __init__(self, config: Dict):
        self.config = config
        self.bgm_config = config.get('audio', {}).get('bgm', {})
        self.library_path = Path("assets/music/background")

    async def select_bgm(
        self,
        category: str,
        mood: str = None,
        duration_needed: float = None
    ) -> Optional[BGMTrack]:
        """
        BGM 선택

        Args:
            category: 카테고리
            mood: 분위기
            duration_needed: 필요한 길이

        Returns:
            선택된 BGM 트랙
        """
        # 분위기 결정
        if not mood:
            moods = self.CATEGORY_MOODS.get(category, ["ambient"])
            mood = random.choice(moods)

        # 라이브러리에서 검색
        tracks = await self._search_library(category, mood)

        if not tracks:
            # 폴백: 기본 트랙
            tracks = await self._get_default_tracks()

        if not tracks:
            return None

        # 길이 조건에 맞는 트랙 필터링
        if duration_needed:
            suitable_tracks = [t for t in tracks if t.duration >= duration_needed]
            if suitable_tracks:
                tracks = suitable_tracks

        # 랜덤 선택
        return random.choice(tracks)

    async def _search_library(
        self,
        category: str,
        mood: str
    ) -> List[BGMTrack]:
        """라이브러리 검색"""
        tracks = []

        # 카테고리별 폴더 검색
        category_path = self.library_path / category
        if category_path.exists():
            for file_path in category_path.glob("*.mp3"):
                tracks.append(BGMTrack(
                    path=str(file_path),
                    name=file_path.stem,
                    category=category,
                    mood=mood,
                    duration=await self._get_duration(file_path),
                    tempo="medium",
                    license="royalty_free"
                ))

        # 분위기별 폴더 검색
        mood_path = self.library_path / mood
        if mood_path.exists():
            for file_path in mood_path.glob("*.mp3"):
                tracks.append(BGMTrack(
                    path=str(file_path),
                    name=file_path.stem,
                    category=category,
                    mood=mood,
                    duration=await self._get_duration(file_path),
                    tempo="medium",
                    license="royalty_free"
                ))

        return tracks

    async def _get_default_tracks(self) -> List[BGMTrack]:
        """기본 트랙"""
        default_path = self.library_path / "default"
        if not default_path.exists():
            return []

        return [
            BGMTrack(
                path=str(file_path),
                name=file_path.stem,
                category="default",
                mood="neutral",
                duration=await self._get_duration(file_path),
                tempo="medium",
                license="royalty_free"
            )
            for file_path in default_path.glob("*.mp3")
        ]

    async def _get_duration(self, file_path: Path) -> float:
        """오디오 길이"""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(str(file_path))
            return len(audio) / 1000
        except Exception:
            return 180.0  # 기본값 3분

    def get_available_moods(self, category: str) -> List[str]:
        """사용 가능한 분위기"""
        return self.CATEGORY_MOODS.get(category, ["ambient", "minimal"])

    async def analyze_track(self, track_path: str) -> Dict:
        """트랙 분석"""
        return {
            "tempo": "medium",
            "energy": 0.5,
            "mood": "neutral"
        }
