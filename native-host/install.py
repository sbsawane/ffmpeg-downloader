#!/usr/bin/env python3
"""
Cross-Platform Installer for FFmpeg Stream Downloader
Supports: Windows, macOS, Linux
Browsers: Chrome, Firefox
"""

import os
import sys
import json
import shutil
import platform
import subprocess
import argparse
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.RESET}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.RESET}")

def print_header(msg):
    print(f"\n{Colors.BOLD}{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}{Colors.RESET}\n")

# Get paths based on OS
def get_native_host_dirs():
    """Get native messaging host directories for each browser/OS combo"""
    system = platform.system()
    home = Path.home()
    
    if system == 'Windows':
        return {
            'chrome': None,  # Windows uses registry
            'firefox': None,  # Windows uses registry
            'type': 'registry'
        }
    elif system == 'Darwin':  # macOS
        return {
            'chrome': home / 'Library' / 'Application Support' / 'Google' / 'Chrome' / 'NativeMessagingHosts',
            'firefox': home / 'Library' / 'Application Support' / 'Mozilla' / 'NativeMessagingHosts',
            'type': 'file'
        }
    else:  # Linux
        return {
            'chrome': home / '.config' / 'google-chrome' / 'NativeMessagingHosts',
            'firefox': home / '.mozilla' / 'native-messaging-hosts',
            'type': 'file'
        }

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    ffmpeg_path = shutil.which('ffmpeg')
    
    if ffmpeg_path:
        print_success(f"FFmpeg found: {ffmpeg_path}")
        # Get version
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            version_line = result.stdout.split('\n')[0]
            print_info(f"Version: {version_line}")
        except:
            pass
        return True
    else:
        # Check common locations
        if platform.system() == 'Windows':
            common_paths = [
                'C:\\ffmpeg\\ffmpeg.exe',
                'C:\\ffmpeg\\bin\\ffmpeg.exe',
            ]
        elif platform.system() == 'Darwin':
            common_paths = [
                '/opt/homebrew/bin/ffmpeg',
                '/usr/local/bin/ffmpeg',
            ]
        else:
            common_paths = ['/usr/bin/ffmpeg']
        
        for path in common_paths:
            if os.path.exists(path):
                print_success(f"FFmpeg found: {path}")
                return True
        
        print_error("FFmpeg not found!")
        print_info("Install FFmpeg:")
        if platform.system() == 'Windows':
            print("  - Download from https://ffmpeg.org/download.html")
            print("  - Extract to C:\\ffmpeg")
            print("  - Add C:\\ffmpeg\\bin to PATH")
        elif platform.system() == 'Darwin':
            print("  - Using Homebrew: brew install ffmpeg")
        else:
            print("  - Ubuntu/Debian: sudo apt install ffmpeg")
            print("  - Fedora: sudo dnf install ffmpeg")
        return False

def check_python_dependencies():
    """Check and install Python dependencies"""
    print_info("Checking Python dependencies...")
    
    try:
        import psutil
        print_success("psutil is installed")
    except ImportError:
        print_warning("psutil not found, installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'psutil'], check=True)
        print_success("psutil installed successfully")

def create_venv():
    """Create and setup virtual environment"""
    venv_path = Path(__file__).parent / 'venv'
    
    if venv_path.exists():
        print_info("Virtual environment already exists")
        return venv_path
    
    print_info("Creating virtual environment...")
    subprocess.run([sys.executable, '-m', 'venv', str(venv_path)], check=True)
    print_success("Virtual environment created")
    
    # Install requirements
    if platform.system() == 'Windows':
        pip_path = venv_path / 'Scripts' / 'pip'
    else:
        pip_path = venv_path / 'bin' / 'pip'
    
    req_file = Path(__file__).parent / 'requirements.txt'
    if req_file.exists():
        print_info("Installing requirements...")
        subprocess.run([str(pip_path), 'install', '-r', str(req_file)], check=True)
        print_success("Requirements installed")
    
    return venv_path

def install_windows_registry(browser, extension_id=None):
    """Install native host on Windows via registry"""
    import winreg
    
    script_dir = Path(__file__).parent
    host_name = 'com.my_downloader'
    
    if browser == 'chrome':
        reg_path = f'Software\\Google\\Chrome\\NativeMessagingHosts\\{host_name}'
        manifest_file = script_dir / 'com.my_downloader.json'
    else:  # firefox
        reg_path = f'Software\\Mozilla\\NativeMessagingHosts\\{host_name}'
        manifest_file = script_dir / 'com.my_downloader.firefox.json'
    
    # Update manifest with correct path
    manifest_data = {
        "name": host_name,
        "description": "FFmpeg Native Host",
        "path": str(script_dir / 'start_host.bat'),
        "type": "stdio"
    }
    
    if browser == 'chrome':
        manifest_data["allowed_origins"] = [f"chrome-extension://{extension_id}/"] if extension_id else ["chrome-extension://YOUR_EXTENSION_ID/"]
    else:
        manifest_data["allowed_extensions"] = [extension_id] if extension_id else ["ffmpeg-downloader@example.com"]
    
    with open(manifest_file, 'w') as f:
        json.dump(manifest_data, f, indent=2)
    
    # Add registry key
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        winreg.SetValueEx(key, '', 0, winreg.REG_SZ, str(manifest_file))
        winreg.CloseKey(key)
        print_success(f"{browser.title()} native host registered in registry")
        return True
    except Exception as e:
        print_error(f"Failed to register: {e}")
        return False

def install_unix_manifest(browser, dirs, extension_id=None):
    """Install native host on Mac/Linux via manifest file"""
    script_dir = Path(__file__).parent
    host_name = 'com.my_downloader'
    target_dir = dirs[browser]
    
    # Create target directory
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Create manifest
    manifest_data = {
        "name": host_name,
        "description": "FFmpeg Native Host",
        "path": str(script_dir / 'start_host.sh'),
        "type": "stdio"
    }
    
    if browser == 'chrome':
        manifest_data["allowed_origins"] = [f"chrome-extension://{extension_id}/"] if extension_id else ["chrome-extension://YOUR_EXTENSION_ID/"]
    else:
        manifest_data["allowed_extensions"] = [extension_id] if extension_id else ["ffmpeg-downloader@example.com"]
    
    manifest_file = target_dir / f'{host_name}.json'
    with open(manifest_file, 'w') as f:
        json.dump(manifest_data, f, indent=2)
    
    # Make start script executable
    start_script = script_dir / 'start_host.sh'
    if start_script.exists():
        os.chmod(start_script, 0o755)
    
    print_success(f"{browser.title()} native host installed")
    print_info(f"Manifest: {manifest_file}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Install FFmpeg Stream Downloader native host')
    parser.add_argument('--browser', choices=['chrome', 'firefox', 'both'], default='both',
                        help='Browser to install for (default: both)')
    parser.add_argument('--extension-id', help='Extension ID (optional, can be set later)')
    parser.add_argument('--venv', action='store_true', help='Create virtual environment')
    parser.add_argument('--check', action='store_true', help='Only check dependencies')
    
    args = parser.parse_args()
    
    print_header("FFmpeg Stream Downloader - Cross-Platform Installer")
    
    print_info(f"Platform: {platform.system()} {platform.release()}")
    print_info(f"Python: {sys.version.split()[0]}")
    print()
    
    # Check FFmpeg
    print_header("Checking FFmpeg")
    ffmpeg_ok = check_ffmpeg()
    
    # Check Python dependencies
    print_header("Checking Python Dependencies")
    check_python_dependencies()
    
    if args.check:
        print_header("Check Complete")
        return 0 if ffmpeg_ok else 1
    
    # Create venv if requested
    if args.venv:
        print_header("Setting up Virtual Environment")
        create_venv()
    
    # Install native hosts
    print_header("Installing Native Host")
    
    dirs = get_native_host_dirs()
    browsers = ['chrome', 'firefox'] if args.browser == 'both' else [args.browser]
    
    for browser in browsers:
        print_info(f"Installing for {browser.title()}...")
        
        if dirs['type'] == 'registry':
            # Windows
            install_windows_registry(browser, args.extension_id)
        else:
            # Mac/Linux
            install_unix_manifest(browser, dirs, args.extension_id)
    
    # Final instructions
    print_header("Installation Complete!")
    
    print("Next steps:")
    print()
    print("1. Load the browser extension:")
    if platform.system() == 'Windows':
        print("   Chrome: chrome://extensions → Load unpacked → select 'extension' folder")
        print("   Firefox: about:debugging → Load Temporary Add-on → select manifest-firefox.json")
    else:
        print("   Chrome: chrome://extensions → Load unpacked → select 'extension' folder")
        print("   Firefox: about:debugging → Load Temporary Add-on → select manifest-firefox.json")
    print()
    print("2. Get your extension ID and update the manifest:")
    
    if dirs['type'] == 'registry':
        script_dir = Path(__file__).parent
        print(f"   Edit: {script_dir / 'com.my_downloader.json'}")
    else:
        for browser in browsers:
            manifest_path = dirs[browser] / 'com.my_downloader.json'
            print(f"   {browser.title()}: {manifest_path}")
    
    print()
    print("3. Restart the browser")
    print()
    
    if not ffmpeg_ok:
        print_warning("Remember to install FFmpeg before using the extension!")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
