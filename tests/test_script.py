"""Tests for script module."""
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestScriptGenerator:
    """Test suite for ScriptGenerator."""

    def test_init(self, config):
        """Test ScriptGenerator initialization."""
        from src.script import ScriptGenerator

        generator = ScriptGenerator(config)
        assert generator.config == config

    @pytest.mark.asyncio
    async def test_generate_without_api(self, config):
        """Test script generation without API."""
        from src.script import ScriptGenerator

        generator = ScriptGenerator(config)
        generator.client = None

        research_data = {
            "topic": "양자역학",
            "facts": ["양자역학은 미시세계를 설명합니다"],
            "sources": []
        }

        result = await generator.generate(research_data, style="kurzgesagt")

        assert isinstance(result, dict)
        assert "script" in result


class TestHookCreator:
    """Test suite for HookCreator."""

    def test_init(self, config):
        """Test HookCreator initialization."""
        from src.script import HookCreator

        creator = HookCreator(config)
        assert creator.config == config

    @pytest.mark.asyncio
    async def test_create_without_api(self, config):
        """Test hook creation without API."""
        from src.script import HookCreator

        creator = HookCreator(config)
        creator.client = None

        hook = await creator.create("양자역학의 신비")

        assert isinstance(hook, str)
        assert len(hook) > 0


class TestCTAGenerator:
    """Test suite for CTAGenerator."""

    def test_init(self, config):
        """Test CTAGenerator initialization."""
        from src.script import CTAGenerator

        generator = CTAGenerator(config)
        assert generator.config == config

    @pytest.mark.asyncio
    async def test_generate_without_api(self, config):
        """Test CTA generation without API."""
        from src.script import CTAGenerator

        generator = CTAGenerator(config)
        generator.client = None

        cta = await generator.generate("과학 영상")

        assert isinstance(cta, dict)
        assert "subscribe" in cta
