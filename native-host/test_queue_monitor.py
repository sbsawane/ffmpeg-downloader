#!/usr/bin/env python3
"""Test the queue-based monitor with actual video URL"""
import subprocess
import threading
import re
import os
import queue

process_info = {}

def test_queue_monitor():
    test_url = "https://vdownload-47.sb-cd.com/1/4/14737616-720p.mp4?secure=Wmb7Ku3ZWoP8F3vKDQkMBg,1769506956&m=47&d=1&_tid=14737616"
    output_file = "C:\\Users\\sande\\Downloads\\test-queue-monitor.mp4"
    
    ffmpeg_cmd = [
        'C:\\ffmpeg\\ffmpeg.exe',
        '-loglevel', 'info',
        '-y',
        '-i', test_url,
        '-t', '10',
        '-c', 'copy',
        '-movflags', '+faststart',
        '-progress', 'pipe:1',
        output_file
    ]
    
    print("[TEST] Starting FFmpeg...")
    
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
    
    # Output queue for non-blocking reads
    output_queue = queue.Queue()
    
    def read_process_output(process, output_queue):
        """Read process output line by line and put in queue"""
        try:
            for line in process.stdout:
                if line:
                    output_queue.put(line.strip())
        except:
            pass
        finally:
            output_queue.put(None)  # Signal end of output
    
    def monitor_process(p, path, pid):
        try:
            duration_seconds = None
            bitrate_kbps = None
            estimated_size = 0
            
            print(f"[MONITOR] Started for PID {pid}")
            
            # Process queue output
            line_count = 0
            while True:
                try:
                    line = output_queue.get(timeout=0.5)
                except queue.Empty:
                    # Check if process is still running
                    if p.poll() is not None:
                        break
                    continue
                
                if line is None:
                    break
                
                if line:
                    line_count += 1
                    if line_count <= 20:
                        print(f"[FFMPEG {line_count}] {line[:80]}")
                    
                    # Extract duration and bitrate
                    if 'Duration:' in line:
                        if duration_seconds is None:
                            match = re.search(r'Duration:\s*(\d+):(\d+):([\d.]+)', line)
                            if match:
                                h = int(match.group(1))
                                m = int(match.group(2))
                                s = float(match.group(3))
                                duration_seconds = h * 3600 + m * 60 + s
                                print(f"\n[DEBUG] Duration: {duration_seconds:.1f} seconds")
                        
                        if bitrate_kbps is None:
                            match = re.search(r'bitrate:\s*([\d.]+)\s*kb/s', line)
                            if match:
                                bitrate_kbps = float(match.group(1))
                                print(f"[DEBUG] Bitrate: {bitrate_kbps} kb/s")
                    
                    # Calculate estimated size
                    if duration_seconds and bitrate_kbps and estimated_size == 0:
                        estimated_size = int((bitrate_kbps * 1000 / 8) * duration_seconds)
                        process_info[pid] = {'estimated_size': estimated_size}
                        print(f"[DEBUG] Estimated file size: {estimated_size / (1024*1024):.2f} MB\n")
            
            print(f"\n[MONITOR] Finished reading {line_count} lines")
            print(f"[MONITOR] Final: duration={duration_seconds}, bitrate={bitrate_kbps}")
            
            p.wait()
            if p.returncode == 0:
                print(f"[SUCCESS] File downloaded")
                if os.path.exists(path):
                    actual_size = os.path.getsize(path)
                    print(f"[INFO] Actual file size: {actual_size / (1024*1024):.2f} MB")
            else:
                print(f"[ERROR] FFmpeg failed with code {p.returncode}")
        except Exception as e:
            print(f"[ERROR] Monitor failed: {e}")
            import traceback
            print(traceback.format_exc())
    
    # Start output reader thread (daemon)
    reader_thread = threading.Thread(target=read_process_output, args=(process, output_queue), daemon=True)
    reader_thread.start()
    
    # Start monitor thread
    monitor_thread = threading.Thread(target=monitor_process, args=(process, output_file, pid), daemon=True)
    monitor_thread.start()
    
    print("[TEST] Waiting for threads...\n")
    monitor_thread.join(timeout=120)
    reader_thread.join(timeout=10)
    
    print(f"\n[TEST] Final process_info: {process_info}")

if __name__ == "__main__":
    test_queue_monitor()
