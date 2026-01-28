#!/bin/bash
# Native host launcher for Mac/Linux
# Use python with unbuffered output for native messaging

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 -u "$SCRIPT_DIR/host.py" 2>&1
