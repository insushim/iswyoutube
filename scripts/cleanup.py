#!/usr/bin/env python
"""Cleanup script for removing temporary and generated files."""
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime, timedelta


def get_size(path: Path) -> int:
    """Get total size of directory or file."""
    if path.is_file():
        return path.stat().st_size
    total = 0
    for p in path.rglob("*"):
        if p.is_file():
            total += p.stat().st_size
    return total


def format_size(size: int) -> str:
    """Format size in human readable format."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def main():
    """Run cleanup tasks."""
    print("=" * 50)
    print("AI Knowledge YouTube Generator - Cleanup")
    print("=" * 50)

    project_root = Path(__file__).parent.parent
    total_freed = 0

    # 1. Clean __pycache__
    print("\n[1/5] Cleaning Python cache...")
    cache_dirs = list(project_root.rglob("__pycache__"))
    for cache_dir in cache_dirs:
        size = get_size(cache_dir)
        total_freed += size
        shutil.rmtree(cache_dir)
    print(f"  ✓ Removed {len(cache_dirs)} __pycache__ directories")

    # 2. Clean .pyc files
    print("\n[2/5] Cleaning .pyc files...")
    pyc_files = list(project_root.rglob("*.pyc"))
    for pyc_file in pyc_files:
        size = pyc_file.stat().st_size
        total_freed += size
        pyc_file.unlink()
    print(f"  ✓ Removed {len(pyc_files)} .pyc files")

    # 3. Clean temp files
    print("\n[3/5] Cleaning temporary files...")
    temp_patterns = ["*.tmp", "*.temp", "*.log", ".DS_Store", "Thumbs.db"]
    temp_count = 0
    for pattern in temp_patterns:
        for temp_file in project_root.rglob(pattern):
            if "logs" not in str(temp_file):  # Keep log files in logs/
                size = temp_file.stat().st_size
                total_freed += size
                temp_file.unlink()
                temp_count += 1
    print(f"  ✓ Removed {temp_count} temporary files")

    # 4. Clean old outputs (optional)
    print("\n[4/5] Checking output directory...")
    output_dir = project_root / "output"
    if output_dir.exists():
        output_size = get_size(output_dir)
        print(f"  Output directory size: {format_size(output_size)}")
        print("  (Run with --clean-output to remove)")

    # 5. Clean old backups
    print("\n[5/5] Checking old backups...")
    backup_dir = project_root / "backups"
    if backup_dir.exists():
        old_backups = []
        cutoff = datetime.now() - timedelta(days=30)
        for backup in backup_dir.iterdir():
            if backup.is_dir():
                mtime = datetime.fromtimestamp(backup.stat().st_mtime)
                if mtime < cutoff:
                    old_backups.append(backup)

        if old_backups:
            print(f"  Found {len(old_backups)} backups older than 30 days")
            print("  (Run with --clean-backups to remove)")
        else:
            print("  ✓ No old backups to clean")

    # Summary
    print("\n" + "=" * 50)
    print(f"Cleanup Complete! Freed: {format_size(total_freed)}")
    print("=" * 50)

    # Handle command line args
    if "--clean-output" in sys.argv:
        print("\nCleaning output directory...")
        if output_dir.exists():
            size = get_size(output_dir)
            shutil.rmtree(output_dir)
            output_dir.mkdir()
            print(f"  ✓ Freed {format_size(size)}")

    if "--clean-backups" in sys.argv:
        print("\nCleaning old backups...")
        for backup in old_backups:
            size = get_size(backup)
            shutil.rmtree(backup)
            print(f"  ✓ Removed {backup.name} ({format_size(size)})")


if __name__ == "__main__":
    main()
