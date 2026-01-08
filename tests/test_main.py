"""Tests for main VideoGenerator class."""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path


class TestVideoGenerator:
    """Test suite for VideoGenerator class."""

    def test_video_generator_init(self, config):
        """Test VideoGenerator initialization."""
        from src.main import VideoGenerator

        with patch.object(VideoGenerator, '_load_config', return_value=config):
            generator = VideoGenerator(config_path="test_config.yaml")
            assert generator.config is not None

    def test_video_category_enum(self):
        """Test VideoCategory enum values."""
        from src.main import VideoCategory

        assert VideoCategory.SCIENCE.value == "science"
        assert VideoCategory.TECHNOLOGY.value == "technology"
        assert VideoCategory.HISTORY.value == "history"

    def test_video_style_enum(self):
        """Test VideoStyle enum values."""
        from src.main import VideoStyle

        assert VideoStyle.KURZGESAGT.value == "kurzgesagt"
        assert VideoStyle.VERITASIUM.value == "veritasium"

    def test_language_enum(self):
        """Test Language enum values."""
        from src.main import Language

        assert Language.KOREAN.value == "ko"
        assert Language.ENGLISH.value == "en"
        assert Language.JAPANESE.value == "ja"

    def test_project_status_enum(self):
        """Test ProjectStatus enum values."""
        from src.main import ProjectStatus

        assert ProjectStatus.CREATED.value == "created"
        assert ProjectStatus.COMPLETED.value == "completed"


class TestVideoProject:
    """Test suite for VideoProject dataclass."""

    def test_video_project_creation(self):
        """Test VideoProject creation."""
        from src.main import VideoProject, VideoCategory, VideoStyle, Language

        project = VideoProject(
            id="test_001",
            topic="테스트 주제",
            category=VideoCategory.SCIENCE,
            style=VideoStyle.KURZGESAGT,
            language=Language.KOREAN
        )

        assert project.id == "test_001"
        assert project.topic == "테스트 주제"
        assert project.category == VideoCategory.SCIENCE


class TestSeriesProject:
    """Test suite for SeriesProject dataclass."""

    def test_series_project_creation(self):
        """Test SeriesProject creation."""
        from src.main import SeriesProject, VideoCategory, VideoStyle, Language

        series = SeriesProject(
            id="series_001",
            title="우주 시리즈",
            topic="우주의 미스터리",
            category=VideoCategory.SCIENCE,
            style=VideoStyle.KURZGESAGT,
            language=Language.KOREAN,
            episode_count=5
        )

        assert series.id == "series_001"
        assert series.episode_count == 5
        assert len(series.episodes) == 0
