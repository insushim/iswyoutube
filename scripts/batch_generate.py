#!/usr/bin/env python
"""Batch generate multiple videos from a topic list."""
import asyncio
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


async def generate_batch(topics_file: str, output_dir: str, parallel: int = 1):
    """Generate videos in batch."""
    from src.main import VideoGenerator, VideoCategory, VideoStyle, Language

    # Load topics
    topics_path = Path(topics_file)
    if not topics_path.exists():
        print(f"Error: Topics file not found: {topics_file}")
        return

    with open(topics_path, 'r', encoding='utf-8') as f:
        if topics_path.suffix == '.json':
            topics_data = json.load(f)
        else:
            # Plain text, one topic per line
            topics_data = [{"topic": line.strip()} for line in f if line.strip()]

    print(f"Loaded {len(topics_data)} topics")

    # Initialize generator
    generator = VideoGenerator()

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Generate results
    results = []
    start_time = datetime.now()

    for i, topic_info in enumerate(topics_data):
        topic = topic_info.get("topic", topic_info) if isinstance(topic_info, dict) else topic_info
        category = topic_info.get("category", "science") if isinstance(topic_info, dict) else "science"
        style = topic_info.get("style", "kurzgesagt") if isinstance(topic_info, dict) else "kurzgesagt"

        print(f"\n[{i+1}/{len(topics_data)}] Generating: {topic}")

        try:
            project = await generator.generate_video(
                topic=topic,
                category=VideoCategory(category),
                style=VideoStyle(style),
                language=Language.KOREAN
            )

            results.append({
                "topic": topic,
                "status": "success",
                "project_id": project.id,
                "video_path": project.video_path,
                "thumbnail_path": project.thumbnail_path
            })
            print(f"  ✓ Success: {project.id}")

        except Exception as e:
            results.append({
                "topic": topic,
                "status": "failed",
                "error": str(e)
            })
            print(f"  ✗ Failed: {e}")

    # Save results
    end_time = datetime.now()
    duration = end_time - start_time

    results_file = output_path / f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "duration_seconds": duration.total_seconds(),
            "total": len(topics_data),
            "success": len([r for r in results if r["status"] == "success"]),
            "failed": len([r for r in results if r["status"] == "failed"]),
            "results": results
        }, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"Batch Generation Complete!")
    print(f"{'='*50}")
    print(f"Total: {len(topics_data)}")
    print(f"Success: {len([r for r in results if r['status'] == 'success'])}")
    print(f"Failed: {len([r for r in results if r['status'] == 'failed'])}")
    print(f"Duration: {duration}")
    print(f"Results saved to: {results_file}")


def main():
    parser = argparse.ArgumentParser(description="Batch generate videos")
    parser.add_argument("topics_file", help="Path to topics file (JSON or TXT)")
    parser.add_argument("--output", "-o", default="output/batch", help="Output directory")
    parser.add_argument("--parallel", "-p", type=int, default=1, help="Parallel generation count")

    args = parser.parse_args()

    asyncio.run(generate_batch(args.topics_file, args.output, args.parallel))


if __name__ == "__main__":
    main()
