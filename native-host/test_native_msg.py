#!/usr/bin/env python3
"""Test host.py with native messaging simulation"""
import json
import sys
import struct
import subprocess
import time
import threading

def send_message(msg):
    """Send a message via native messaging protocol"""
    msg_json = json.dumps(msg)
    msg_bytes = msg_json.encode('utf-8')
    length = len(msg_bytes)
    sys.stdout.write(struct.pack('I', length))
    sys.stdout.write(msg_bytes)
    sys.stdout.flush()

def read_message():
    """Read a message via native messaging protocol"""
    try:
        raw_length = sys.stdin.read(4)
        if not raw_length or len(raw_length) < 4:
            return None
        length = struct.unpack('I', raw_length)[0]
        msg_bytes = sys.stdin.read(length)
        msg_json = msg_bytes.decode('utf-8')
        return json.loads(msg_json)
    except Exception as e:
        print(f"[ERROR] read_message failed: {e}", file=sys.stderr)
        return None

def main():
    print("[TEST] Starting host.py simulation...", file=sys.stderr)
    
    # Start host.py process
    host_proc = subprocess.Popen(
        [sys.executable, "host.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="F:\\Projects\\ffmpeg-downloader\\native-host"
    )
    
    print(f"[TEST] host.py started with PID {host_proc.pid}", file=sys.stderr)
    time.sleep(0.5)
    
    # Replace stdio
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = open(host_proc.stdout.fileno(), 'rb', buffering=1)
    sys.stdout = open(host_proc.stdin.fileno(), 'wb', buffering=1)
    
    try:
        # Send download request
        test_url = "https://vdownload-47.sb-cd.com/1/4/14737616-720p.mp4?secure=Wmb7Ku3ZWoP8F3vKDQkMBg,1769506956&m=47&d=1&_tid=14737616"
        send_message({"url": test_url, "filename": "test-native-msg.mp4"})
        print("[TEST] Sent download request", file=sys.stderr)
        
        time.sleep(1)
        response = read_message()
        if response:
            print(f"[TEST] Got response: {response}", file=sys.stderr)
            pid = response.get("pid")
        else:
            print("[TEST] No response from host", file=sys.stderr)
            return
        
        # Poll progress 15 times
        for i in range(15):
            time.sleep(1)
            send_message({"command": "get-progress", "pid": pid})
            progress = read_message()
            if progress:
                dl = progress.get('downloaded', 0)
                total = progress.get('estimated_total', 0)
                pct = int((dl / total * 100)) if total > 0 else 0
                print(f"[TEST-{i}] {pct}% | {dl/(1024*1024):.2f} MB / {total/(1024*1024):.2f} MB", file=sys.stderr)
        
        print("[TEST] Complete", file=sys.stderr)
        
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        host_proc.terminate()
        host_proc.wait(timeout=5)

if __name__ == "__main__":
    main()
