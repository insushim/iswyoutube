"""
Audio Mixer Module
==================
Mix multiple audio tracks together
"""

from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class MixResult:
    """믹싱 결과"""
    output_path: str
    duration: float
    tracks_used: List[str]
    settings: Dict


class AudioMixer:
    """오디오 믹서"""

    def __init__(self, config: Dict):
        self.config = config
        self.bgm_config = config.get('audio', {}).get('bgm', {})

    async def mix(
        self,
        narration_path: str,
        bgm_path: str = None,
        sfx_list: List[Dict] = None,
        output_path: str = None
    ) -> MixResult:
        """
        오디오 믹싱

        Args:
            narration_path: 나레이션 경로
            bgm_path: BGM 경로
            sfx_list: 효과음 리스트 [{"path": "", "position": seconds}]
            output_path: 출력 경로

        Returns:
            믹싱 결과
        """
        if not output_path:
            output_path = str(Path(narration_path).parent / "mixed_audio.mp3")

        try:
            from pydub import AudioSegment

            # 나레이션 로드
            narration = AudioSegment.from_file(narration_path)
            total_duration = len(narration)

            tracks_used = [narration_path]

            # BGM 추가
            if bgm_path and Path(bgm_path).exists():
                bgm = AudioSegment.from_file(bgm_path)

                # BGM 볼륨 조절
                volume = self.bgm_config.get('volume', 0.15)
                volume_db = 20 * (volume - 1)  # dB 변환
                bgm = bgm + volume_db

                # BGM 길이 조절
                if len(bgm) < total_duration:
                    loops_needed = (total_duration // len(bgm)) + 1
                    bgm = bgm * loops_needed
                bgm = bgm[:total_duration]

                # 페이드 인/아웃
                fade_in_ms = int(self.bgm_config.get('fade_in', 2.0) * 1000)
                fade_out_ms = int(self.bgm_config.get('fade_out', 3.0) * 1000)
                bgm = bgm.fade_in(fade_in_ms).fade_out(fade_out_ms)

                # 믹싱
                narration = narration.overlay(bgm)
                tracks_used.append(bgm_path)

            # 효과음 추가
            if sfx_list:
                for sfx in sfx_list:
                    sfx_path = sfx.get('path')
                    position_ms = int(sfx.get('position', 0) * 1000)

                    if sfx_path and Path(sfx_path).exists():
                        sfx_audio = AudioSegment.from_file(sfx_path)
                        sfx_volume = sfx.get('volume', 0.3)
                        sfx_audio = sfx_audio + (20 * (sfx_volume - 1))

                        if position_ms < total_duration:
                            narration = narration.overlay(sfx_audio, position=position_ms)
                            tracks_used.append(sfx_path)

            # 저장
            narration.export(output_path, format="mp3")

            return MixResult(
                output_path=output_path,
                duration=total_duration / 1000,
                tracks_used=tracks_used,
                settings={
                    "bgm_volume": self.bgm_config.get('volume', 0.15),
                    "fade_in": self.bgm_config.get('fade_in', 2.0),
                    "fade_out": self.bgm_config.get('fade_out', 3.0),
                }
            )
        except ImportError:
            raise RuntimeError("pydub not installed")
        except Exception as e:
            raise RuntimeError(f"Audio mixing failed: {e}")

    async def apply_ducking(
        self,
        mixed_path: str,
        narration_path: str,
        output_path: str = None
    ) -> str:
        """
        음성 기반 BGM 더킹

        나레이션이 있을 때 BGM 볼륨을 낮춤
        """
        ducking_config = self.bgm_config.get('ducking', {})

        if not ducking_config.get('enabled', True):
            return mixed_path

        # 실제 구현은 복잡한 오디오 분석 필요
        # 여기서는 간단한 폴백
        return mixed_path

    async def normalize_audio(
        self,
        audio_path: str,
        target_lufs: float = -14,
        output_path: str = None
    ) -> str:
        """오디오 정규화"""
        try:
            from pydub import AudioSegment

            audio = AudioSegment.from_file(audio_path)

            # 간단한 정규화
            target_dbfs = -14
            change_in_dbfs = target_dbfs - audio.dBFS
            normalized = audio.apply_gain(change_in_dbfs)

            if not output_path:
                output_path = audio_path.replace(".mp3", "_normalized.mp3")

            normalized.export(output_path, format="mp3")
            return output_path
        except Exception:
            return audio_path
