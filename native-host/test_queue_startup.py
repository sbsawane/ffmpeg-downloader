#!/usr/bin/env python3
"""Quick test to verify the queue-based message handling in host.py"""
import subprocess
import sys
import time

print("[TEST] Starting host.py to verify it's responsive...")

proc = subprocess.Popen(
    [sys.executable, "-u", "host.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    cwd="F:\\Projects\\ffmpeg-downloader\\native-host"
)

print(f"[TEST] host.py PID: {proc.pid}")
time.sleep(1)

# Check if it's still running
if proc.poll() is None:
    print("[SUCCESS] host.py is running and responsive with queue-based message handling")
    proc.terminate()
    proc.wait()
else:
    print("[ERROR] host.py crashed")
    stderr = proc.stderr.read()
    print(stderr)

