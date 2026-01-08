"""
TTS Engine Module
=================
Text-to-Speech generation using gTTS (Google Text-to-Speech) - Free
"""

from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass
import os


@dataclass
class TTSResult:
    """TTS 결과"""
    audio_path: str
    duration: float
    voice_id: str
    provider: str
    segments_timing: List[Dict]


class TTSEngine:
    """TTS 엔진 - gTTS 무료 버전 사용"""

    LANGUAGE_CODES = {
        "ko": "ko",
        "en": "en",
        "ja": "ja",
        "zh": "zh-CN",
        "es": "es",
        "fr": "fr",
        "de": "de",
        "pt": "pt",
        "ru": "ru",
        "ar": "ar",
    }

    def __init__(self, config: Dict):
        self.config = config
        self.tts_config = config.get('audio', {}).get('tts', {})

    async def generate(
        self,
        text: str,
        language: str = "ko",
        voice_id: str = None,
        output_path: str = None,
        provider: str = None
    ) -> TTSResult:
        """
        TTS 생성 - gTTS 사용

        Args:
            text: 변환할 텍스트
            language: 언어
            voice_id: 음성 ID (gTTS에서는 사용 안함)
            output_path: 출력 경로
            provider: 제공자 (무시됨)

        Returns:
            TTS 결과
        """
        if not output_path:
            output_path = f"output/audio/tts_{language}.mp3"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        lang_code = self.LANGUAGE_CODES.get(language, "en")

        try:
            from gtts import gTTS

            tts = gTTS(text=text, lang=lang_code, slow=False)
            tts.save(output_path)

            duration = await self._get_audio_duration(output_path)

            return TTSResult(
                audio_path=output_path,
                duration=duration,
                voice_id=lang_code,
                provider="gtts",
                segments_timing=[]
            )
        except Exception as e:
            print(f"gTTS error: {e}")
            # 빈 파일 생성
            Path(output_path).touch()
            return TTSResult(
                audio_path=output_path,
                duration=0.0,
                voice_id=lang_code,
                provider="gtts",
                segments_timing=[]
            )

    async def _get_audio_duration(self, audio_path: str) -> float:
        """오디오 길이 계산"""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000  # ms to seconds
        except Exception:
            return 0.0

    def get_available_voices(self, language: str) -> List[Dict]:
        """사용 가능한 음성 목록"""
        return [
            {"id": self.LANGUAGE_CODES.get(language, "en"), "type": "default"}
        ]
