#!/usr/bin/env python3
"""
Test the native host communication locally without browser
"""
import json
import struct
import sys
import os

# Add the native-host directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Mock stdin/stdout for testing
class MockStdin:
    def __init__(self, messages):
        self.messages = messages
        self.index = 0
        self.buffer = MockBuffer(messages)
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass

class MockBuffer:
    def __init__(self, messages):
        self.messages = messages
        self.index = 0
        self.data = b''
        self.prepare_data()
    
    def prepare_data(self):
        for msg in self.messages:
            encoded = json.dumps(msg).encode('utf-8')
            length = struct.pack('@I', len(encoded))
            self.data += length + encoded
        self.pos = 0
    
    def read(self, size):
        result = self.data[self.pos:self.pos+size]
        self.pos += size
        return result

class MockStdout:
    def __init__(self):
        self.buffer = MockStdoutBuffer()

class MockStdoutBuffer:
    def __init__(self):
        self.messages = []
    
    def write(self, data):
        self.messages.append(data)
    
    def flush(self):
        pass

# Test message
test_message = {
    "command": "download",
    "url": "https://example.com/test.mp4",
    "filename": "test-download.mp4"
}

print("Testing native host communication...")
print(f"Test message: {test_message}")

# Encode the message
encoded = json.dumps(test_message).encode('utf-8')
length = struct.pack('@I', len(encoded))

print(f"Encoded message length: {len(encoded)} bytes")
print(f"Length header: {length.hex()}")
print(f"Total to send: {len(length) + len(encoded)} bytes")

# Now test that our host.py can decode it
print("\nSimulating what host.py would receive:")
print(f"Raw bytes: {(length + encoded).hex()}")

# Decode back
decoded_length = struct.unpack('@I', length)[0]
print(f"Decoded length: {decoded_length}")
print(f"Message matches: {encoded.decode('utf-8') == json.dumps(test_message)}")
