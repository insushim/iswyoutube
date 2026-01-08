"""Dubbing Engine - Generate dubbed audio for different languages"""
from typing import Dict
from pathlib import Path

class DubbingEngine:
    def __init__(self, config: Dict):
        self.config = config
        self.tts_config = config.get('audio', {}).get('tts', {})

    async def dub(self, text: str, language: str, output_path: str = None) -> str:
        if not output_path:
            output_path = f"output/audio/dub_{language}.mp3"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        try:
            from elevenlabs import ElevenLabs, VoiceSettings
            client = ElevenLabs()
            voice_id = self.tts_config.get('voices', {}).get(language, {}).get('male', '')
            if not voice_id: return ""
            audio = client.text_to_speech.convert(voice_id=voice_id, text=text, model_id="eleven_multilingual_v2")
            with open(output_path, 'wb') as f:
                for chunk in audio: f.write(chunk)
            return output_path
        except: return ""

    async def match_timing(self, original_audio: str, dubbed_audio: str) -> str:
        return dubbed_audio
