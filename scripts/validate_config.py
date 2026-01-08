#!/usr/bin/env python
"""Validate configuration files."""
import os
import sys
from pathlib import Path

import yaml


def validate_settings(settings_path: Path) -> list:
    """Validate settings.yaml file."""
    errors = []

    if not settings_path.exists():
        return [f"Settings file not found: {settings_path}"]

    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML parsing error: {e}"]

    # Required sections
    required_sections = ["channel", "video", "audio", "visual", "api"]
    for section in required_sections:
        if section not in config:
            errors.append(f"Missing required section: {section}")

    # Validate channel
    if "channel" in config:
        channel = config["channel"]
        if "name" not in channel:
            errors.append("channel.name is required")
        if "language" not in channel:
            errors.append("channel.language is required")

    # Validate video settings
    if "video" in config:
        video = config["video"]
        if "resolution" in video:
            valid_res = ["720p", "1080p", "4k"]
            if video["resolution"] not in valid_res:
                errors.append(f"video.resolution must be one of {valid_res}")
        if "fps" in video:
            valid_fps = [24, 30, 60]
            if video["fps"] not in valid_fps:
                errors.append(f"video.fps must be one of {valid_fps}")

    # Validate audio settings
    if "audio" in config:
        audio = config["audio"]
        if "tts" in audio:
            tts = audio["tts"]
            valid_providers = ["elevenlabs", "openai", "google"]
            if "provider" in tts and tts["provider"] not in valid_providers:
                errors.append(f"audio.tts.provider must be one of {valid_providers}")

    return errors


def validate_api_keys(env_path: Path) -> list:
    """Validate API keys file."""
    errors = []
    warnings = []

    if not env_path.exists():
        return [f"API keys file not found: {env_path}"], []

    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Required keys
    required_keys = ["ANTHROPIC_API_KEY"]
    optional_keys = ["OPENAI_API_KEY", "ELEVENLABS_API_KEY"]

    for key in required_keys:
        if key not in content or f"{key}=your_" in content or f"{key}=" in content.split('\n'):
            errors.append(f"Required API key not set: {key}")

    for key in optional_keys:
        if key not in content or f"{key}=your_" in content:
            warnings.append(f"Optional API key not set: {key}")

    return errors, warnings


def main():
    """Run validation."""
    print("=" * 50)
    print("Configuration Validation")
    print("=" * 50)

    project_root = Path(__file__).parent.parent
    all_valid = True

    # Validate settings.yaml
    print("\n[1/2] Validating settings.yaml...")
    settings_path = project_root / "config" / "settings.yaml"
    settings_errors = validate_settings(settings_path)

    if settings_errors:
        all_valid = False
        for error in settings_errors:
            print(f"  ✗ {error}")
    else:
        print("  ✓ settings.yaml is valid")

    # Validate API keys
    print("\n[2/2] Validating api_keys.env...")
    env_path = project_root / "config" / "api_keys.env"
    api_errors, api_warnings = validate_api_keys(env_path)

    if api_errors:
        all_valid = False
        for error in api_errors:
            print(f"  ✗ {error}")
    else:
        print("  ✓ Required API keys are set")

    if api_warnings:
        for warning in api_warnings:
            print(f"  ⚠ {warning}")

    # Summary
    print("\n" + "=" * 50)
    if all_valid:
        print("✓ All configurations are valid!")
        sys.exit(0)
    else:
        print("✗ Configuration errors found. Please fix them.")
        sys.exit(1)


if __name__ == "__main__":
    main()
