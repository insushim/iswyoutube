#!/usr/bin/env python
"""
AI Knowledge YouTube Video Generator - Quick Start
===================================================

Usage:
    python run.py generate "양자역학의 기초"
    python run.py generate "블랙홀" --style kurzgesagt
    python run.py series "우주의 미스터리" --episodes 5
    python run.py suggest --category science --count 10
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import main

if __name__ == "__main__":
    main()
