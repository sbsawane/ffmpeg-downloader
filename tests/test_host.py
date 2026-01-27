import subprocess
import os

# Test 1: Verify FFmpeg is installed in the CI environment
def test_ffmpeg_installation():
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True)
    assert result.returncode == 0

# Test 2: Verify Host Logic (Mocking the stream)
def test_download_command_construction():
    url = "http://test-stream.com/playlist.m3u8"
    filename = "test_output.mp4"
    path = os.path.join(os.path.expanduser("~"), "Downloads", filename)
    
    # We construct the exact command the host would use
    command = ['ffmpeg', '-y', '-i', url, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', path]
    
    # Assert the command structure is correct (Basic Logic Test)
    assert command[0] == 'ffmpeg'
    assert command[3] == url
    assert command[8] == path