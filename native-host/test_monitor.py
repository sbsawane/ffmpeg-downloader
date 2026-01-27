#!/usr/bin/env python3
"""Test the monitor thread with actual FFmpeg"""
import subprocess
import threading
import time
import re
import os

process_info = {}
active_processes = {}
active_downloads = {}

def test_monitor():
    # Use a real video file from downloads
    test_file = os.path.expanduser("~/Downloads/test-source.mp4")
    if not os.path.exists(test_file):
        print(f"Test file not found: {test_file}")
        return
    
    output_file = os.path.expanduser("~/Downloads/test-monitor-output.mp4")
    
    # Simple FFmpeg command to copy the test file
    ffmpeg_cmd = [
        'C:\\ffmpeg\\ffmpeg.exe',
        '-loglevel', 'info',
        '-i', test_file,
        '-t', '5',  # Only 5 seconds
        '-c', 'copy',
        '-progress', 'pipe:1',
        output_file
    ]
    
    print(f"Running: {' '.join(ffmpeg_cmd[:5])}... (truncated)")
    print(f"Output file: {output_file}\n")
    
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
    active_processes[pid] = process
    active_downloads[pid] = output_file
    
    print(f"Process started with PID: {pid}\n")
    
    # Monitor function
    def monitor_process(p, path, pid):
        print(f"[MONITOR] Starting monitor thread for PID {pid}")
        try:
            duration_seconds = None
            bitrate_kbps = None
            line_count = 0
            
            for line in p.stdout:
                line = line.strip()
                if not line:
                    continue
                
                line_count += 1
                if line_count <= 20:  # Print first 20 lines
                    print(f"[FFMPEG {line_count}] {line[:80]}")
                
                # Extract duration
                if 'Duration:' in line and duration_seconds is None:
                    match = re.search(r'Duration:\s*(\d+):(\d+):([\d.]+)', line)
                    if match:
                        hours = int(match.group(1))
                        minutes = int(match.group(2))
                        seconds = float(match.group(3))
                        duration_seconds = hours * 3600 + minutes * 60 + seconds
                        print(f"\n[DEBUG] Extracted duration: {duration_seconds:.1f} seconds\n")
                
                # Extract bitrate
                if 'bitrate:' in line and bitrate_kbps is None:
                    match = re.search(r'bitrate:\s*([\d.]+)\s*kb/s', line)
                    if match:
                        bitrate_kbps = float(match.group(1))
                        print(f"[DEBUG] Extracted bitrate: {bitrate_kbps} kb/s\n")
            
            print(f"\n[MONITOR] Read {line_count} lines total")
            print(f"[MONITOR] Final: duration={duration_seconds}, bitrate={bitrate_kbps}")
            print(f"[MONITOR] Calculation check: duration and bitrate = {bool(duration_seconds and bitrate_kbps)}")
            
            # Calculate estimated size
            if duration_seconds and bitrate_kbps:
                estimated_size = int((bitrate_kbps * 1000 / 8) * duration_seconds)
                process_info[pid] = {'estimated_size': estimated_size}
                print(f"[MONITOR] Calculated estimated size: {estimated_size / (1024*1024):.2f} MB")
            else:
                print(f"[MONITOR] Skipped calculation: duration={duration_seconds}, bitrate={bitrate_kbps}")
            
            p.wait()
            print(f"[MONITOR] Process finished with return code: {p.returncode}")
            
        except Exception as e:
            print(f"[ERROR] Monitor failed: {e}")
            import traceback
            print(traceback.format_exc())
        finally:
            print("[MONITOR] Cleaning up")
    
    # Start monitor as daemon
    monitor_thread = threading.Thread(target=monitor_process, args=(process, output_file, pid), daemon=True)
    monitor_thread.start()
    
    # Wait for monitor to finish
    monitor_thread.join(timeout=60)
    print(f"\n[TEST] Monitor thread finished. process_info: {process_info}")
    
    # Check result
    if os.path.exists(output_file):
        size = os.path.getsize(output_file)
        print(f"[TEST] Output file created: {size} bytes ({size/(1024*1024):.2f} MB)")
    else:
        print("[TEST] Output file was NOT created")

if __name__ == "__main__":
    test_monitor()
