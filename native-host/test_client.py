#!/usr/bin/env python3
"""Test native message passing to host.py"""
import json
import sys
import struct
import time
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
    
    print(f"[CLIENT] Sent: {msg}", file=sys.stderr)

def read_message():
    """Read a message from host.py"""
    # Read length (4 bytes)
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        return None
    
    length = struct.unpack('I', raw_length)[0]
    msg_bytes = sys.stdin.buffer.read(length)
    msg_json = msg_bytes.decode('utf-8')
    msg = json.loads(msg_json)
    
    print(f"[CLIENT] Received: {msg}", file=sys.stderr)
    return msg

def main():
    print("[CLIENT] Starting test client", file=sys.stderr)
    
    # Send a download request
    send_message({
        "url": "https://commondatastorage.googleapis.com/gtv-videos-library/sample/ForBiggerBlazes.mp4",
        "filename": "test-from-client.mp4"
    })
    
    time.sleep(1)
    
    # Try to read response
    print("[CLIENT] Waiting for response...", file=sys.stderr)
    response = read_message()
    if response:
        print(f"[CLIENT] Got response: {response}", file=sys.stderr)
    else:
        print("[CLIENT] No response", file=sys.stderr)
    
    # Get progress a few times
    for i in range(5):
        time.sleep(2)
        send_message({"command": "get-progress", "pid": response.get("pid") if response else 0})
        progress = read_message()
        if progress:
            print(f"[CLIENT] Progress {i}: {progress}", file=sys.stderr)

if __name__ == "__main__":
    main()
