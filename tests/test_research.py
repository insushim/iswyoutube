"""Tests for research module."""
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestTopicGenerator:
    """Test suite for TopicGenerator."""

    def test_init(self, config):
        """Test TopicGenerator initialization."""
        from src.research import TopicGenerator

        generator = TopicGenerator(config)
        assert generator.config == config

    @pytest.mark.asyncio
    async def test_generate_without_api(self, config):
        """Test topic generation without API."""
        from src.research import TopicGenerator

        generator = TopicGenerator(config)
        generator.client = None  # Simulate no API

        topics = await generator.generate("science", count=3)

        assert isinstance(topics, list)
        assert len(topics) == 3


class TestTrendAnalyzer:
    """Test suite for TrendAnalyzer."""

    def test_init(self, config):
        """Test TrendAnalyzer initialization."""
        from src.research import TrendAnalyzer

        analyzer = TrendAnalyzer(config)
        assert analyzer.config == config

    @pytest.mark.asyncio
    async def test_analyze_without_api(self, config):
        """Test trend analysis without API."""
        from src.research import TrendAnalyzer

        analyzer = TrendAnalyzer(config)
        analyzer.client = None

        trends = await analyzer.analyze("artificial intelligence")

        assert isinstance(trends, dict)
        assert "keywords" in trends


class TestFactChecker:
    """Test suite for FactChecker."""

    def test_init(self, config):
        """Test FactChecker initialization."""
        from src.research import FactChecker

        checker = FactChecker(config)
        assert checker.config == config

    @pytest.mark.asyncio
    async def test_check_without_api(self, config):
        """Test fact checking without API."""
        from src.research import FactChecker

        checker = FactChecker(config)
        checker.client = None

        result = await checker.check(["The Earth is round"])

        assert isinstance(result, dict)
        assert "verified" in result
