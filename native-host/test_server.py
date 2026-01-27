#!/usr/bin/env python3
"""
Simple HTTP server for testing downloads
Serves test video file so you can verify the entire download pipeline works
"""
import http.server
import socketserver
import os
from pathlib import Path

PORT = 8000
TEST_FILE = r"C:\Users\sande\Downloads\test-source.mp4"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/test-video.mp4":
            # Serve the test video
            if os.path.exists(TEST_FILE):
                size = os.path.getsize(TEST_FILE)
                self.send_response(200)
                self.send_header("Content-Type", "video/mp4")
                self.send_header("Content-Length", str(size))
                self.send_header("Accept-Ranges", "bytes")
                self.end_headers()
                
                with open(TEST_FILE, 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Test file not found")
                return
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found. Use /test-video.mp4")

if __name__ == "__main__":
    print(f"Starting test server on http://127.0.0.1:{PORT}")
    print(f"Video URL: http://127.0.0.1:{PORT}/test-video.mp4")
    print(f"Serving: {TEST_FILE}")
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Server running... Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
