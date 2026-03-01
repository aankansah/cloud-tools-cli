#!/bin/bash
# Cloud Tools Wrapper Script
# This script activates the virtual environment and runs cloud-tools

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_PATH="$SCRIPT_DIR/venv"

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Virtual environment not found at: $VENV_PATH"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -e ."
    exit 1
fi

# Activate virtual environment and run cloud-tools
source "$VENV_PATH/bin/activate"
python -m cloud_tools.cli "$@"
