#!/usr/bin/env python3
import subprocess
import os

# Test with a public small test file
url = "https://commondatastorage.googleapis.com/gtv-videos-library/sample/ForBiggerBlazes.mp4"
output_path = "C:\\Users\\sande\\Downloads\\test-public-video.mp4"

print(f"Testing FFmpeg download with public video...")
print(f"URL: {url}")
print(f"Output: {output_path}")

ffmpeg_cmd = [
    'C:\\ffmpeg\\ffmpeg.exe',
    '-loglevel', 'verbose',
    '-http_user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    '-y',
    '-i', url,
    '-c', 'copy',
    '-movflags', '+faststart',
    output_path
]

print(f"\nRunning: {' '.join(ffmpeg_cmd)}\n")

try:
    # Don't use PIPE to see live output
    process = subprocess.Popen(ffmpeg_cmd)
    process.wait(timeout=60)
    print(f"\nProcess finished with return code: {process.returncode}")
    
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"Output file size: {size} bytes ({size/1024/1024:.2f} MB)")
    else:
        print("Output file was not created")
        
except subprocess.TimeoutExpired:
    print("Download timed out after 60 seconds")
    process.kill()
except Exception as e:
    print(f"Error: {e}")

