#!/usr/bin/env python3
"""Direct test of the monitor thread logic from host.py"""
import subprocess
import threading
import re
import os
import time

# Simulate the process_info dict
process_info = {}

def log_message(msg):
    """Simple logging"""
    print(msg)

def test_direct():
    """Test the exact logic from host.py with actual URL"""
    # Use actual video URL from user
    test_url = "https://vdownload-47.sb-cd.com/1/4/14737616-720p.mp4?secure=Wmb7Ku3ZWoP8F3vKDQkMBg,1769506956&m=47&d=1&_tid=14737616"
    output_file = "C:\\Users\\sande\\Downloads\\test-actual-url-monitor.mp4"
    
    # Build exact FFmpeg command from host.py
    ffmpeg_cmd = [
        'C:\\ffmpeg\\ffmpeg.exe',
        '-loglevel', 'info',
        '-y',
        '-i', test_url,
        '-t', '10',  # Only first 10 seconds for testing
        '-c', 'copy',
        '-movflags', '+faststart',
        '-progress', 'pipe:1',
        output_file
    ]
    
    print(f"[TEST] Starting FFmpeg: {' '.join(ffmpeg_cmd[:8])}...")
    
    # Create subprocess with exact config from host.py
    process = subprocess.Popen(
        ffmpeg_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1,
        shell=False
    )
    
    pid = process.pid
    print(f"[TEST] Process started with PID: {pid}\n")
    
    # Monitor function - EXACT COPY from host.py
    def monitor_process(p, path, pid):
        try:
            duration_seconds = None
            bitrate_kbps = None
            estimated_size = 0
            
            print(f"[MONITOR] Started reading from PID {pid}")
            line_count = 0
            
            # Read FFmpeg output line by line
            for line in p.stdout:
                line = line.strip()
                if not line:
                    continue
                
                line_count += 1
                log_message(f"[FFMPEG] {line}")
                
                # Extract duration and bitrate from FFmpeg output
                # Format: Duration: HH:MM:SS.ms, start: X.XX, bitrate: XXX kb/s
                if 'Duration:' in line:
                    # Extract duration
                    if duration_seconds is None:
                        match = re.search(r'Duration:\s*(\d+):(\d+):([\d.]+)', line)
                        if match:
                            hours = int(match.group(1))
                            minutes = int(match.group(2))
                            seconds = float(match.group(3))
                            duration_seconds = hours * 3600 + minutes * 60 + seconds
                            log_message(f"[DEBUG] Detected duration: {duration_seconds:.1f} seconds")
                    
                    # Extract bitrate from same line (format: "bitrate: XXX kb/s")
                    if bitrate_kbps is None:
                        match = re.search(r'bitrate:\s*([\d.]+)\s*kb/s', line)
                        if match:
                            bitrate_kbps = float(match.group(1))
                            log_message(f"[DEBUG] Detected bitrate: {bitrate_kbps} kb/s")
                
                # Calculate estimated size once we have both duration and bitrate
                if duration_seconds and bitrate_kbps and estimated_size == 0:
                    estimated_size = int((bitrate_kbps * 1000 / 8) * duration_seconds)
                    process_info[pid] = {'estimated_size': estimated_size}
                    log_message(f"[DEBUG] Estimated file size: {estimated_size / (1024*1024):.2f} MB")
            
            print(f"[MONITOR] Finished reading. Total lines: {line_count}")
            print(f"[MONITOR] Final: duration={duration_seconds}, bitrate={bitrate_kbps}")
            print(f"[MONITOR] process_info: {process_info}")
            
            p.wait()
            if p.returncode == 0:
                log_message(f"[SUCCESS] File downloaded: {path}")
                try:
                    actual_size = os.path.getsize(path)
                    log_message(f"[INFO] Actual file size: {actual_size / (1024*1024):.2f} MB")
                except:
                    pass
            else:
                log_message(f"[ERROR] FFmpeg failed with code {p.returncode}")
        except Exception as e:
            log_message(f"[ERROR] Monitor failed: {str(e)}")
            import traceback
            log_message(traceback.format_exc())
    
    # Start monitor as non-daemon thread
    monitor_thread = threading.Thread(target=monitor_process, args=(process, output_file, pid), daemon=False)
    monitor_thread.start()
    
    print("[TEST] Monitor thread started, waiting for it to finish...\n")
    monitor_thread.join()
    
    print(f"\n[TEST] Final process_info: {process_info}")

if __name__ == "__main__":
    test_direct()
