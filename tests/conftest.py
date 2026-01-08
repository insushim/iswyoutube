"""Pytest configuration and fixtures."""
import pytest
import asyncio
from pathlib import Path
from typing import Dict, Any

# Test configuration
TEST_CONFIG: Dict[str, Any] = {
    "channel": {
        "name": "Test Channel",
        "language": "ko"
    },
    "video": {
        "default_length": 600,
        "resolution": "1080p",
        "fps": 30
    },
    "audio": {
        "tts": {
            "provider": "mock",
            "voice_id": "test_voice"
        }
    },
    "visual": {
        "provider": "mock"
    },
    "api": {
        "anthropic": {"model": "claude-sonnet-4-20250514"},
        "openai": {"model": "gpt-4o-mini"}
    }
}


@pytest.fixture
def config():
    """Provide test configuration."""
    return TEST_CONFIG.copy()


@pytest.fixture
def temp_output_dir(tmp_path):
    """Create temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


@pytest.fixture
def sample_script():
    """Provide sample video script."""
    return """
    안녕하세요, 오늘은 양자역학에 대해 알아보겠습니다.

    양자역학은 미시세계의 물리법칙을 설명하는 이론입니다.
    원자와 분자 수준에서 일어나는 현상들을 이해하는 데 필수적입니다.

    첫 번째로, 파동-입자 이중성에 대해 살펴보겠습니다.
    빛은 파동이면서 동시에 입자의 성질을 가지고 있습니다.

    다음 영상에서 더 자세히 알아보겠습니다.
    구독과 좋아요 부탁드립니다!
    """


@pytest.fixture
def sample_project_data():
    """Provide sample project data."""
    return {
        "id": "test_project_001",
        "topic": "양자역학의 기초",
        "category": "science",
        "style": "kurzgesagt",
        "language": "ko",
        "status": "created"
    }


@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
