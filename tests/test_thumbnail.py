"""Tests for thumbnail module."""
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestThumbnailGenerator:
    """Test suite for ThumbnailGenerator."""

    def test_init(self, config):
        """Test ThumbnailGenerator initialization."""
        from src.thumbnail import ThumbnailGenerator

        generator = ThumbnailGenerator(config)
        assert generator.config == config

    @pytest.mark.asyncio
    async def test_generate(self, config, temp_output_dir):
        """Test thumbnail generation."""
        from src.thumbnail import ThumbnailGenerator

        generator = ThumbnailGenerator(config)

        result = await generator.generate(
            title="테스트 제목",
            style="kurzgesagt",
            output_path=str(temp_output_dir / "thumbnail.png")
        )

        assert result is not None


class TestThumbnailABTester:
    """Test suite for ThumbnailABTester."""

    def test_init(self, config):
        """Test ThumbnailABTester initialization."""
        from src.thumbnail import ThumbnailABTester

        tester = ThumbnailABTester(config)
        assert tester.config == config


class TestCTRPredictor:
    """Test suite for CTRPredictor."""

    def test_init(self, config):
        """Test CTRPredictor initialization."""
        from src.thumbnail import CTRPredictor

        predictor = CTRPredictor(config)
        assert predictor.config == config

    @pytest.mark.asyncio
    async def test_predict(self, config):
        """Test CTR prediction."""
        from src.thumbnail import CTRPredictor

        predictor = CTRPredictor(config)

        result = await predictor.predict(
            thumbnail_path="test.png",
            title="흥미로운 제목"
        )

        assert isinstance(result, dict)
        assert "score" in result
