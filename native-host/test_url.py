#!/usr/bin/env python3
"""Test host.py with actual video URL via native messaging"""
import json
import sys
import struct
import time
import subprocess
import threading

def send_message(msg):
    """Send a message to host.py via native messaging"""
    msg_json = json.dumps(msg)
    msg_bytes = msg_json.encode('utf-8')
    length = len(msg_bytes)
    
    # Write length (4 bytes, little-endian)
    sys.stdout.buffer.write(struct.pack('I', length))
    sys.stdout.buffer.flush()
    
    # Write message
    sys.stdout.buffer.write(msg_bytes)
    sys.stdout.buffer.flush()
    
    print(f"[CLIENT] Sent: {msg['url'][:80] if 'url' in msg else msg}", file=sys.stderr)

def read_message():
    """Read a message from host.py"""
    try:
        # Read length (4 bytes)
        raw_length = sys.stdin.buffer.read(4)
        if not raw_length:
            return None
        
        length = struct.unpack('I', raw_length)[0]
        msg_bytes = sys.stdin.buffer.read(length)
        msg_json = msg_bytes.decode('utf-8')
        msg = json.loads(msg_json)
        
        return msg
    except:
        return None

def main():
    print("[CLIENT] Starting test with actual video URL", file=sys.stderr)
    print("[CLIENT] Connecting to host.py...", file=sys.stderr)
    
    # Start host.py
    host_process = subprocess.Popen(
        [sys.executable, "host.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd="F:\\Projects\\ffmpeg-downloader\\native-host"
    )
    
    print(f"[CLIENT] host.py started with PID {host_process.pid}", file=sys.stderr)
    time.sleep(0.5)
    
    # Replace stdin/stdout with host process pipes
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    sys.stdin = open(host_process.stdout.fileno(), 'rb', buffering=0)
    sys.stdout = open(host_process.stdin.fileno(), 'wb', buffering=0)
    sys.stderr = open("test_url_log.txt", 'w')
    
    try:
        # Send download request with actual URL
        send_message({
            "url": "https://vdownload-47.sb-cd.com/1/4/14737616-720p.mp4?secure=Wmb7Ku3ZWoP8F3vKDQkMBg,1769506956&m=47&d=1&_tid=14737616",
            "filename": "test-actual-url.mp4"
        })
        
        time.sleep(1)
        
        # Read response
        print("[CLIENT] Waiting for response...", file=sys.stderr)
        response = read_message()
        if response:
            print(f"[CLIENT] Got response: {response}", file=sys.stderr)
            pid = response.get("pid")
        else:
            print("[CLIENT] No response", file=sys.stderr)
            return
        
        # Get progress several times
        for i in range(10):
            time.sleep(2)
            send_message({"command": "get-progress", "pid": pid})
            progress = read_message()
            if progress:
                print(f"[CLIENT] Progress {i}: downloaded={progress.get('downloaded')} estimated={progress.get('estimated_total')}", file=sys.stderr)
            else:
                print(f"[CLIENT] No progress response {i}", file=sys.stderr)
        
        print("[CLIENT] Test complete", file=sys.stderr)
        
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        
        host_process.terminate()
        host_process.wait(timeout=5)

if __name__ == "__main__":
    main()
