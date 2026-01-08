#!/bin/bash
# AI Knowledge YouTube Video Generator - Unix Runner
# Usage: ./run.sh generate "Your Topic"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate venv if exists
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# Run the generator
python "$SCRIPT_DIR/run.py" "$@"
