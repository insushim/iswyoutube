"""Tests for audio module."""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path


class TestTTSEngine:
    """Test suite for TTSEngine."""

    def test_init(self, config):
        """Test TTSEngine initialization."""
        from src.audio import TTSEngine

        engine = TTSEngine(config)
        assert engine.config == config

    def test_provider_selection(self, config):
        """Test TTS provider selection."""
        from src.audio import TTSEngine

        config["audio"] = {"tts": {"provider": "elevenlabs"}}
        engine = TTSEngine(config)

        assert engine.provider == "elevenlabs"


class TestBGMSelector:
    """Test suite for BGMSelector."""

    def test_init(self, config):
        """Test BGMSelector initialization."""
        from src.audio import BGMSelector

        selector = BGMSelector(config)
        assert selector.config == config

    @pytest.mark.asyncio
    async def test_select(self, config):
        """Test BGM selection."""
        from src.audio import BGMSelector

        selector = BGMSelector(config)
        result = await selector.select("upbeat", duration=60)

        assert result is not None


class TestAudioMixer:
    """Test suite for AudioMixer."""

    def test_init(self, config):
        """Test AudioMixer initialization."""
        from src.audio import AudioMixer

        mixer = AudioMixer(config)
        assert mixer.config == config


class TestAudioEnhancer:
    """Test suite for AudioEnhancer."""

    def test_init(self, config):
        """Test AudioEnhancer initialization."""
        from src.audio import AudioEnhancer

        enhancer = AudioEnhancer(config)
        assert enhancer.config == config
