#!/usr/bin/env python
"""Generate a sample video to test the system."""
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


async def main():
    """Generate sample video."""
    print("=" * 50)
    print("Sample Video Generation")
    print("=" * 50)

    from src.main import VideoGenerator, VideoCategory, VideoStyle, Language

    # Initialize generator
    print("\n[1/5] Initializing generator...")
    try:
        generator = VideoGenerator()
        print("  ✓ Generator initialized")
    except Exception as e:
        print(f"  ✗ Failed to initialize: {e}")
        return

    # Sample topics
    sample_topics = [
        ("양자역학 입문: 슈뢰딩거의 고양이 이해하기", VideoCategory.SCIENCE),
        ("인공지능의 미래: 2030년 예측", VideoCategory.TECHNOLOGY),
        ("고대 로마의 멸망: 5가지 핵심 원인", VideoCategory.HISTORY),
    ]

    topic, category = sample_topics[0]

    # Generate video
    print(f"\n[2/5] Topic: {topic}")
    print(f"       Category: {category.value}")
    print(f"       Style: kurzgesagt")

    print("\n[3/5] Starting generation pipeline...")

    try:
        project = await generator.generate_video(
            topic=topic,
            category=category,
            style=VideoStyle.KURZGESAGT,
            language=Language.KOREAN
        )

        print("\n[4/5] Generation complete!")
        print(f"  Project ID: {project.id}")
        print(f"  Status: {project.status.value}")

        if project.video_path:
            print(f"  Video: {project.video_path}")
        if project.thumbnail_path:
            print(f"  Thumbnail: {project.thumbnail_path}")

        print("\n[5/5] Summary")
        print("=" * 50)
        print("✓ Sample video generated successfully!")

    except Exception as e:
        print(f"\n✗ Generation failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
