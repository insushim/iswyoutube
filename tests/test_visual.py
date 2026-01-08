"""Tests for visual module."""
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestImageGenerator:
    """Test suite for ImageGenerator."""

    def test_init(self, config):
        """Test ImageGenerator initialization."""
        from src.visual import ImageGenerator

        generator = ImageGenerator(config)
        assert generator.config == config

    @pytest.mark.asyncio
    async def test_generate_placeholder(self, config, temp_output_dir):
        """Test placeholder image generation."""
        from src.visual import ImageGenerator

        generator = ImageGenerator(config)
        generator.client = None  # No API

        result = await generator.generate(
            prompt="A beautiful sunset",
            output_path=str(temp_output_dir / "test.png")
        )

        assert result is not None


class TestScenePlanner:
    """Test suite for ScenePlanner."""

    def test_init(self, config):
        """Test ScenePlanner initialization."""
        from src.visual import ScenePlanner

        planner = ScenePlanner(config)
        assert planner.config == config

    @pytest.mark.asyncio
    async def test_plan_scenes(self, config, sample_script):
        """Test scene planning."""
        from src.visual import ScenePlanner

        planner = ScenePlanner(config)
        planner.client = None

        scenes = await planner.plan(sample_script)

        assert isinstance(scenes, list)


class TestChartGenerator:
    """Test suite for ChartGenerator."""

    def test_init(self, config):
        """Test ChartGenerator initialization."""
        from src.visual import ChartGenerator

        generator = ChartGenerator(config)
        assert generator.config == config

    @pytest.mark.asyncio
    async def test_generate_bar_chart(self, config, temp_output_dir):
        """Test bar chart generation."""
        from src.visual import ChartGenerator

        generator = ChartGenerator(config)

        data = {
            "labels": ["A", "B", "C"],
            "values": [10, 20, 30]
        }

        result = await generator.generate(
            chart_type="bar",
            data=data,
            output_path=str(temp_output_dir / "chart.png")
        )

        assert result is not None
