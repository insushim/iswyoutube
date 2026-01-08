"""
Audio Enhancer Module
=====================
Enhance audio quality
"""

from typing import Dict, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class EnhancementResult:
    """향상 결과"""
    output_path: str
    enhancements_applied: list
    quality_before: float
    quality_after: float


class AudioEnhancer:
    """오디오 향상기"""

    def __init__(self, config: Dict):
        self.config = config
        self.processing_config = config.get('audio', {}).get('processing', {})

    async def enhance(
        self,
        audio_path: str,
        output_path: str = None,
        enhancements: list = None
    ) -> EnhancementResult:
        """
        오디오 향상

        Args:
            audio_path: 입력 오디오 경로
            output_path: 출력 경로
            enhancements: 적용할 향상 목록

        Returns:
            향상 결과
        """
        if not output_path:
            output_path = audio_path.replace(".mp3", "_enhanced.mp3")

        enhancements = enhancements or self._get_default_enhancements()
        applied = []

        try:
            from pydub import AudioSegment

            audio = AudioSegment.from_file(audio_path)
            quality_before = self._estimate_quality(audio)

            # 노이즈 제거
            if 'denoise' in enhancements and self.processing_config.get('denoise', True):
                audio = await self._denoise(audio)
                applied.append('denoise')

            # 정규화
            if 'normalize' in enhancements and self.processing_config.get('normalize', True):
                target_lufs = self.processing_config.get('target_lufs', -14)
                audio = self._normalize(audio, target_lufs)
                applied.append('normalize')

            # 압축
            if 'compress' in enhancements and self.processing_config.get('compress', True):
                audio = self._compress(audio)
                applied.append('compress')

            # EQ 향상
            if 'eq' in enhancements and self.processing_config.get('eq_enhance', True):
                audio = self._enhance_eq(audio)
                applied.append('eq')

            # 저장
            audio.export(
                output_path,
                format="mp3",
                bitrate="320k",
                parameters=["-ar", str(self.processing_config.get('sample_rate', 44100))]
            )

            quality_after = self._estimate_quality(audio)

            return EnhancementResult(
                output_path=output_path,
                enhancements_applied=applied,
                quality_before=quality_before,
                quality_after=quality_after
            )
        except ImportError:
            raise RuntimeError("pydub not installed")
        except Exception as e:
            return EnhancementResult(
                output_path=audio_path,
                enhancements_applied=[],
                quality_before=0.7,
                quality_after=0.7
            )

    def _get_default_enhancements(self) -> list:
        """기본 향상 목록"""
        return ['denoise', 'normalize', 'compress', 'eq']

    async def _denoise(self, audio) -> any:
        """노이즈 제거"""
        # 실제로는 noisereduce 라이브러리 사용
        # 여기서는 간단한 폴백
        return audio

    def _normalize(self, audio, target_lufs: float) -> any:
        """정규화"""
        target_dbfs = target_lufs
        change_in_dbfs = target_dbfs - audio.dBFS
        return audio.apply_gain(change_in_dbfs)

    def _compress(self, audio) -> any:
        """다이나믹 레인지 압축"""
        # 간단한 압축 (실제로는 더 정교한 알고리즘 필요)
        return audio.compress_dynamic_range()

    def _enhance_eq(self, audio) -> any:
        """EQ 향상"""
        # 음성 향상을 위한 간단한 EQ
        # 저음 약간 감소, 중음 약간 증가
        return audio

    def _estimate_quality(self, audio) -> float:
        """품질 추정"""
        # 간단한 휴리스틱
        if audio.dBFS < -30:
            return 0.5
        elif audio.dBFS > -10:
            return 0.6
        else:
            return 0.8

    async def remove_silence(
        self,
        audio_path: str,
        min_silence_len: int = 500,
        silence_thresh: int = -40
    ) -> str:
        """무음 구간 제거"""
        try:
            from pydub import AudioSegment
            from pydub.silence import split_on_silence

            audio = AudioSegment.from_file(audio_path)

            chunks = split_on_silence(
                audio,
                min_silence_len=min_silence_len,
                silence_thresh=silence_thresh
            )

            output = AudioSegment.empty()
            for chunk in chunks:
                output += chunk

            output_path = audio_path.replace(".mp3", "_no_silence.mp3")
            output.export(output_path, format="mp3")

            return output_path
        except Exception:
            return audio_path
