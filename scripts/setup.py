#!/usr/bin/env python
"""Setup script for initial project configuration."""
import os
import sys
import shutil
from pathlib import Path


def main():
    """Run setup tasks."""
    print("=" * 50)
    print("AI Knowledge YouTube Generator - Setup")
    print("=" * 50)

    project_root = Path(__file__).parent.parent

    # 1. Create directories
    print("\n[1/4] Creating directories...")
    directories = [
        "output/videos",
        "output/thumbnails",
        "output/shorts",
        "output/audio",
        "output/repurposed",
        "backups",
        "logs",
        "data/cache",
        "data/projects",
    ]

    for dir_path in directories:
        full_path = project_root / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {dir_path}")

    # 2. Create API keys file
    print("\n[2/4] Setting up configuration...")
    env_example = project_root / "config" / "api_keys.env.example"
    env_file = project_root / "config" / "api_keys.env"

    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("  ✓ Created config/api_keys.env")
        print("  ⚠ Please edit config/api_keys.env with your API keys")
    elif env_file.exists():
        print("  ✓ config/api_keys.env already exists")
    else:
        print("  ⚠ api_keys.env.example not found")

    # 3. Check Python dependencies
    print("\n[3/4] Checking dependencies...")
    try:
        import anthropic
        print("  ✓ anthropic installed")
    except ImportError:
        print("  ✗ anthropic not installed")

    try:
        import openai
        print("  ✓ openai installed")
    except ImportError:
        print("  ✗ openai not installed")

    try:
        import moviepy
        print("  ✓ moviepy installed")
    except ImportError:
        print("  ✗ moviepy not installed")

    try:
        from PIL import Image
        print("  ✓ Pillow installed")
    except ImportError:
        print("  ✗ Pillow not installed")

    # 4. Check FFmpeg
    print("\n[4/4] Checking FFmpeg...")
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        print(f"  ✓ FFmpeg found: {ffmpeg_path}")
    else:
        print("  ✗ FFmpeg not found in PATH")
        print("  ⚠ Please install FFmpeg: https://ffmpeg.org/download.html")

    # Summary
    print("\n" + "=" * 50)
    print("Setup Complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Edit config/api_keys.env with your API keys")
    print("2. Run: python -m src.main generate --topic \"Your Topic\"")
    print("\nFor help: python -m src.main --help")


if __name__ == "__main__":
    main()
