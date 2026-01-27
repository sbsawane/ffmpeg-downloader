#!/usr/bin/env python3
"""Test monitor logic without threading"""
import subprocess
import re
import os

test_file = os.path.expanduser("~/Downloads/test-source.mp4")
output_file = os.path.expanduser("~/Downloads/test-simple-output.mp4")

ffmpeg_cmd = [
    'C:\\ffmpeg\\ffmpeg.exe',
    '-loglevel', 'info',
    '-i', test_file,
    '-t', '3',
    '-c', 'copy',
    '-progress', 'pipe:1',
    output_file
]

print("Starting FFmpeg...")
process = subprocess.Popen(
    ffmpeg_cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True,
    bufsize=1,
)

duration_seconds = None
bitrate_kbps = None
line_count = 0

print("Reading output...")
for line in process.stdout:
    line = line.strip()
    if not line:
        continue
    
    line_count += 1
    
    # First 20 lines
    if line_count <= 20:
        print(f"[{line_count}] {line[:80]}")
    
    # Extract duration
    if 'Duration:' in line:
        print(f"\n==> Found Duration line: {line}")
        if duration_seconds is None:
            match = re.search(r'Duration:\s*(\d+):(\d+):([\d.]+)', line)
            if match:
                h = int(match.group(1))
                m = int(match.group(2))
                s = float(match.group(3))
                duration_seconds = h * 3600 + m * 60 + s
                print(f"==> EXTRACTED DURATION: {duration_seconds} seconds")
    
    # Extract bitrate
    if 'bitrate:' in line:
        print(f"\n==> Found bitrate line: {line}")
        if bitrate_kbps is None:
            match = re.search(r'bitrate:\s*([\d.]+)\s*kb/s', line)
            if match:
                bitrate_kbps = float(match.group(1))
                print(f"==> EXTRACTED BITRATE: {bitrate_kbps} kb/s")

print(f"\n\nFinal results:")
print(f"Lines read: {line_count}")
print(f"Duration: {duration_seconds}")
print(f"Bitrate: {bitrate_kbps}")

if duration_seconds and bitrate_kbps:
    estimated = int((bitrate_kbps * 1000 / 8) * duration_seconds)
    print(f"Estimated size: {estimated} bytes = {estimated/(1024*1024):.2f} MB")
else:
    print("Could not calculate estimated size")

process.wait()
print(f"Process return code: {process.returncode}")

if os.path.exists(output_file):
    size = os.path.getsize(output_file)
    print(f"Output file size: {size} bytes = {size/(1024*1024):.2f} MB")
