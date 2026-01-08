"""
Voice Cloner Module
===================
Clone voices for consistent narration
"""

from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ClonedVoice:
    """복제된 음성"""
    voice_id: str
    name: str
    sample_count: int
    quality_score: float
    provider: str


class VoiceCloner:
    """음성 복제기"""

    def __init__(self, config: Dict):
        self.config = config
        self.clone_config = config.get('audio', {}).get('voice_cloning', {})

    async def clone_voice(
        self,
        sample_paths: List[str],
        voice_name: str,
        description: str = None
    ) -> ClonedVoice:
        """
        음성 복제

        Args:
            sample_paths: 샘플 오디오 경로 리스트
            voice_name: 음성 이름
            description: 설명

        Returns:
            복제된 음성
        """
        min_samples = self.clone_config.get('min_samples', 3)

        if len(sample_paths) < min_samples:
            raise ValueError(f"최소 {min_samples}개의 샘플이 필요합니다")

        try:
            from elevenlabs import ElevenLabs

            client = ElevenLabs()

            # 파일 읽기
            files = []
            for path in sample_paths:
                with open(path, 'rb') as f:
                    files.append(f.read())

            # 음성 복제 (ElevenLabs API)
            voice = client.clone(
                name=voice_name,
                description=description or f"{voice_name} cloned voice",
                files=files
            )

            return ClonedVoice(
                voice_id=voice.voice_id,
                name=voice_name,
                sample_count=len(sample_paths),
                quality_score=0.8,
                provider="elevenlabs"
            )
        except ImportError:
            raise RuntimeError("ElevenLabs not installed")
        except Exception as e:
            raise RuntimeError(f"Voice cloning failed: {e}")

    async def list_cloned_voices(self) -> List[ClonedVoice]:
        """복제된 음성 목록"""
        try:
            from elevenlabs import ElevenLabs

            client = ElevenLabs()
            voices = client.voices.get_all()

            return [
                ClonedVoice(
                    voice_id=v.voice_id,
                    name=v.name,
                    sample_count=0,
                    quality_score=0.8,
                    provider="elevenlabs"
                )
                for v in voices.voices
                if v.category == "cloned"
            ]
        except Exception:
            return []

    async def delete_cloned_voice(self, voice_id: str) -> bool:
        """복제된 음성 삭제"""
        try:
            from elevenlabs import ElevenLabs

            client = ElevenLabs()
            client.voices.delete(voice_id)
            return True
        except Exception:
            return False

    def validate_samples(self, sample_paths: List[str]) -> Dict:
        """샘플 유효성 검증"""
        issues = []

        for path in sample_paths:
            if not Path(path).exists():
                issues.append(f"File not found: {path}")
                continue

            # 파일 크기 체크
            size = Path(path).stat().st_size
            if size < 10000:  # 10KB 미만
                issues.append(f"File too small: {path}")
            if size > 10_000_000:  # 10MB 초과
                issues.append(f"File too large: {path}")

        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "sample_count": len(sample_paths)
        }
