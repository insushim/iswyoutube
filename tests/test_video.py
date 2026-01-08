"""Tests for video module."""
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestVideoComposer:
    """Test suite for VideoComposer."""

    def test_init(self, config):
        """Test VideoComposer initialization."""
        from src.video import VideoComposer

        composer = VideoComposer(config)
        assert composer.config == config


class TestSubtitleGenerator:
    """Test suite for SubtitleGenerator."""

    def test_init(self, config):
        """Test SubtitleGenerator initialization."""
        from src.video import SubtitleGenerator

        generator = SubtitleGenerator(config)
        assert generator.config == config

    @pytest.mark.asyncio
    async def test_generate_srt(self, config, sample_script, temp_output_dir):
        """Test SRT subtitle generation."""
        from src.video import SubtitleGenerator

        generator = SubtitleGenerator(config)

        segments = [
            {"start": 0, "end": 5, "text": "안녕하세요"},
            {"start": 5, "end": 10, "text": "오늘은 양자역학입니다"}
        ]

        result = await generator.generate(
            segments=segments,
            output_path=str(temp_output_dir / "subtitles.srt")
        )

        assert result is not None


class TestTransitionHandler:
    """Test suite for TransitionHandler."""

    def test_init(self, config):
        """Test TransitionHandler initialization."""
        from src.video import TransitionHandler

        handler = TransitionHandler(config)
        assert handler.config == config

    def test_get_transition_types(self, config):
        """Test getting available transition types."""
        from src.video import TransitionHandler

        handler = TransitionHandler(config)
        transitions = handler.get_available_transitions()

        assert "fade" in transitions
        assert "crossfade" in transitions


class TestVideoExporter:
    """Test suite for VideoExporter."""

    def test_init(self, config):
        """Test VideoExporter initialization."""
        from src.video import VideoExporter

        exporter = VideoExporter(config)
        assert exporter.config == config

    def test_supported_formats(self, config):
        """Test supported export formats."""
        from src.video import VideoExporter

        exporter = VideoExporter(config)
        formats = exporter.get_supported_formats()

        assert "mp4" in formats
        assert "webm" in formats
