import sys
import json
import struct
import subprocess
import os
import re
import threading
import signal
from urllib.parse import urlparse
from pathlib import Path

# Setup logs directory
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOG_FILE = LOGS_DIR / "ffmpeg-download.log"
PROGRESS_FILE = LOGS_DIR / "progress.json"

# HELPER: Read message from Chrome (Standard Input)
def get_message():
    """Read a single message from stdin (native messaging protocol)"""
    raw_length = sys.stdin.buffer.read(4)
    if len(raw_length) == 0:
        return None
    message_length = struct.unpack('@I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode('utf-8')
    return json.loads(message)

# HELPER: Send message to Chrome (Standard Output)
def send_message(message_content):
    encoded_content = json.dumps(message_content).encode('utf-8')
    encoded_length = struct.pack('@I', len(encoded_content))
    sys.stdout.buffer.write(encoded_length)
    sys.stdout.buffer.write(encoded_content)
    sys.stdout.buffer.flush()

# HELPER: Log messages
def log_message(message):
    """Write message to log file"""
    try:
        with open(LOG_FILE, 'a') as log:
            log.write(message + '\n')
    except:
        pass

# HELPER: Extract title from URL
def extract_title_from_url(url):
    """Extract a meaningful title from URL"""
    try:
        parsed = urlparse(url)
        path = parsed.path.split('/')[-1]
        if path and path != 'playlist.m3u8':
            return path.split('?')[0]
    except:
        pass
    return None

# HELPER: Parse FFmpeg progress - extract size
def parse_ffmpeg_progress(line, download_path):
    """Parse FFmpeg progress line and return dict with file size"""
    try:
        progress = {}
        
        # Extract time: 00:01:23.45
        time_match = re.search(r'time=(\d{2}):(\d{2}):(\d{2})', line)
        if time_match:
            progress['time'] = f"{time_match.group(1)}:{time_match.group(2)}:{time_match.group(3)}"
        
        # Extract speed: 1.5x
        speed_match = re.search(r'speed=\s*([\d.]+)x', line)
        if speed_match:
            progress['speed'] = f"{speed_match.group(1)}x"
        
        # Check actual file size being written
        if os.path.exists(download_path):
            try:
                file_size = os.path.getsize(download_path)
                progress['downloaded'] = file_size
            except:
                pass
        
        return progress if progress else None
    except:
        return None

# HELPER: Get total file size from FFmpeg output
def extract_duration_and_bitrate(stderr_lines):
    """Extract duration to estimate total size"""
    try:
        for line in stderr_lines:
            # Look for Duration: HH:MM:SS.ms
            duration_match = re.search(r'Duration:\s*(\d+):(\d+):([\d.]+)', line)
            if duration_match:
                hours = int(duration_match.group(1))
                minutes = int(duration_match.group(2))
                seconds = float(duration_match.group(3))
                total_seconds = hours * 3600 + minutes * 60 + seconds
                
                # Look for bitrate
                bitrate_match = re.search(r'bitrate=\s*([\d.]+)\s*kb/s', line)
                if bitrate_match:
                    bitrate_kbps = float(bitrate_match.group(1))
                    estimated_size = (bitrate_kbps * 1000 / 8) * total_seconds  # Convert kb/s to bytes/s
                    return estimated_size
        return None
    except:
        return None

def main():
    try:
        msg = get_message()
        
        if msg is None:
            sys.exit(0)
        
        command = msg.get('command')
        
        # Handle get-progress command - check file size on disk
        if command == 'get-progress':
            pid = msg.get('pid')
            filename = msg.get('filename', '')
            
            # Try to find the file in Downloads folder
            downloads = str(Path.home() / "Downloads")
            
            # If filename provided, use it directly
            if filename:
                download_path = os.path.join(downloads, filename)
                if os.path.exists(download_path):
                    file_size = os.path.getsize(download_path)
                    send_message({
                        "status": "progress",
                        "pid": pid,
                        "downloaded": file_size,
                        "estimated_total": 0
                    })
                    sys.exit(0)
            
            # File not found
            send_message({"status": "error", "message": "File not found"})
            sys.exit(0)
        
        # Handle kill command - kill FFmpeg process by PID
        if command == 'kill':
            pid = msg.get('pid')
            log_message(f"[INFO] Kill request for PID: {pid}")
            
            try:
                os.kill(pid, signal.SIGTERM)
                log_message(f"[SUCCESS] Process {pid} terminated")
                send_message({"status": "killed", "pid": pid})
            except ProcessLookupError:
                log_message(f"[WARNING] Process {pid} not found (already finished)")
                send_message({"status": "killed", "pid": pid})
            except Exception as e:
                log_message(f"[ERROR] Failed to kill process {pid}: {str(e)}")
                send_message({"status": "error", "message": f"Failed to kill: {str(e)}"})
            sys.exit(0)
        
        # Handle download command (default)
        url = msg.get('url')
        filename = msg.get('filename', '')
        
        if not url:
            send_message({"status": "error", "message": "No URL provided"})
            sys.exit(1)
        
        # If no filename provided, try to extract from URL
        if not filename or filename == 'output.mp4':
            extracted = extract_title_from_url(url)
            if extracted:
                filename = extracted
            else:
                filename = 'output.mp4'
        
        # Ensure filename has extension
        if not filename.lower().endswith(('.mp4', '.mkv', '.m3u8', '.ts')):
            filename += '.mp4'
        
        # Determine path
        downloads = str(Path.home() / "Downloads")
        download_path = os.path.join(downloads, filename)
        
        # Avoid overwriting files
        if os.path.exists(download_path):
            name, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(downloads, f"{name}_{counter}{ext}")):
                counter += 1
            download_path = os.path.join(downloads, f"{name}_{counter}{ext}")
        
        log_message(f"\n[INFO] URL: {url}")
        log_message(f"[INFO] Output: {download_path}")
        
        # Start FFmpeg with proper configuration
        ffmpeg_cmd = [
            'C:\\ffmpeg\\ffmpeg.exe',
            '-loglevel', 'info',
            '-y', 
            '-i', url, 
            '-c', 'copy', 
            '-movflags', '+faststart',
            download_path
        ]
        
        # Windows-specific: Detach FFmpeg from native host process
        creationflags = 0
        if sys.platform == 'win32':
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

        process = subprocess.Popen(
            ffmpeg_cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            shell=False,
            creationflags=creationflags
        )
        
        pid = process.pid
        log_message(f"[INFO] FFmpeg started with PID: {pid}")
        
        # Send response immediately - FFmpeg runs independently
        send_message({
            "status": "success", 
            "pid": pid, 
            "path": download_path,
            "filename": os.path.basename(download_path)
        })
        
        # Monitor progress in background thread (logs every 5 seconds)
        def monitor_download(pid, path):
            import time
            import psutil
            
            start_time = time.time()
            last_size = 0
            
            while True:
                time.sleep(5)
                
                # Check if FFmpeg process is still running
                try:
                    proc = psutil.Process(pid)
                    if proc.status() == psutil.STATUS_ZOMBIE or not proc.is_running():
                        break
                except psutil.NoSuchProcess:
                    break
                
                # Get current file size
                try:
                    if os.path.exists(path):
                        current_size = os.path.getsize(path)
                        elapsed = time.time() - start_time
                        
                        # Calculate speed (bytes per second over last 5 sec interval)
                        speed = (current_size - last_size) / 5 if last_size > 0 else current_size / elapsed
                        speed_mbps = (speed * 8) / (1024 * 1024)  # Convert to Mbps
                        
                        size_mb = current_size / (1024 * 1024)
                        
                        log_message(f"[PROGRESS] PID {pid}: {size_mb:.2f} MB downloaded | Speed: {speed_mbps:.2f} Mbps | Elapsed: {int(elapsed)}s")
                        
                        last_size = current_size
                except Exception as e:
                    log_message(f"[WARN] Progress check failed: {e}")
            
            # Final status
            try:
                if os.path.exists(path):
                    final_size = os.path.getsize(path)
                    total_time = time.time() - start_time
                    avg_speed = (final_size * 8) / (total_time * 1024 * 1024) if total_time > 0 else 0
                    log_message(f"[COMPLETE] PID {pid}: {final_size / (1024*1024):.2f} MB | Total time: {int(total_time)}s | Avg speed: {avg_speed:.2f} Mbps")
                else:
                    log_message(f"[ERROR] PID {pid}: Download failed - file not found")
            except Exception as e:
                log_message(f"[ERROR] PID {pid}: Final check failed: {e}")
        
        # Start monitor thread (non-daemon to keep process alive)
        monitor_thread = threading.Thread(target=monitor_download, args=(pid, download_path), daemon=False)
        monitor_thread.start()
        
        # Wait for monitor to complete (keeps host alive while monitoring)
        monitor_thread.join()
        
    except FileNotFoundError as e:
        error_msg = f"FFmpeg not found: {str(e)}"
        log_message(f"[ERROR] {error_msg}")
        send_message({"status": "error", "message": error_msg})
    except Exception as e:
        error_msg = str(e)
        log_message(f"\n[ERROR] {error_msg}")
        import traceback
        log_message(traceback.format_exc())
        try:
            send_message({"status": "error", "message": error_msg})
        except:
            pass

if __name__ == '__main__':
    main()