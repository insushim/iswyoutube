#!/usr/bin/env python
"""Export analytics data to various formats."""
import asyncio
import sys
import json
import csv
import argparse
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


async def export_analytics(output_format: str, output_path: str, days: int = 30):
    """Export analytics data."""
    from src.analytics import YouTubeAnalytics, DashboardGenerator

    print(f"Exporting analytics for last {days} days...")

    # Initialize analytics
    analytics = YouTubeAnalytics({})

    # Get data
    try:
        data = await analytics.get_channel_stats(days=days)
    except Exception as e:
        print(f"Error fetching analytics: {e}")
        # Use sample data for demonstration
        data = {
            "period": f"Last {days} days",
            "views": 0,
            "subscribers": 0,
            "watch_time_hours": 0,
            "videos": []
        }

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if output_format == "json":
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        print(f"✓ Exported to {output_file}")

    elif output_format == "csv":
        if "videos" in data and data["videos"]:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data["videos"][0].keys())
                writer.writeheader()
                writer.writerows(data["videos"])
        else:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["metric", "value"])
                for key, value in data.items():
                    if not isinstance(value, list):
                        writer.writerow([key, value])
        print(f"✓ Exported to {output_file}")

    elif output_format == "html":
        dashboard = DashboardGenerator({})
        html_path = await dashboard.generate(data, str(output_file))
        print(f"✓ Dashboard exported to {html_path}")

    else:
        print(f"Unknown format: {output_format}")


def main():
    parser = argparse.ArgumentParser(description="Export analytics data")
    parser.add_argument("--format", "-f", choices=["json", "csv", "html"], default="json")
    parser.add_argument("--output", "-o", default="output/analytics/export")
    parser.add_argument("--days", "-d", type=int, default=30)

    args = parser.parse_args()

    # Add extension based on format
    output_path = args.output
    if not output_path.endswith(f".{args.format}"):
        output_path = f"{output_path}.{args.format}"

    asyncio.run(export_analytics(args.format, output_path, args.days))


if __name__ == "__main__":
    main()
