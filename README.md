# FFmpeg Stream Downloader

A browser extension + native host that automatically detects video streams and downloads them using FFmpeg.

[![CI](https://github.com/user/ffmpeg-downloader/actions/workflows/ci.yml/badge.svg)](https://github.com/user/ffmpeg-downloader/actions/workflows/ci.yml)

## Features

- 🔍 **Auto-detection** - Automatically detects `.m3u8`, `.mpd`, `.mp4` and other video streams
- 📥 **Queue support** - Download multiple videos simultaneously
- 🚀 **Fast downloads** - Uses FFmpeg with stream copy (no re-encoding)
- 🌐 **Cross-browser** - Works on Chrome (MV3) and Firefox (MV2)
- 📊 **Progress tracking** - Real-time download speed and file size in logs

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         BROWSER                                  │
│  ┌─────────────────┐    ┌─────────────────┐                     │
│  │  background.js  │◄──►│    popup.js     │                     │
│  │  (Service       │    │  (UI & Queue)   │                     │
│  │   Worker)       │    └─────────────────┘                     │
│  └────────┬────────┘                                            │
│           │ Native Messaging                                     │
└───────────┼─────────────────────────────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      NATIVE HOST (Python)                        │
│  ┌─────────────────┐    ┌─────────────────┐                     │
│  │     host.py     │───►│     FFmpeg      │                     │
│  │  (Message       │    │  (Subprocess)   │                     │
│  │   Handler)      │    └─────────────────┘                     │
│  └─────────────────┘                                            │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────┐                                            │
│  │  Downloads/     │  ← Output files                            │
│  │  logs/          │  ← Progress logs                           │
│  └─────────────────┘                                            │
└─────────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- **FFmpeg** installed and available at `C:\ffmpeg\ffmpeg.exe` (or update path in `host.py`)
- **Python 3.9+** with `psutil` package
- **Chrome** or **Firefox** browser

### 1. Install Python Dependencies

```bash
cd native-host
pip install -r requirements.txt
```

### 2. Register Native Host

**Windows (Chrome):**
```batch
cd native-host
install_host.bat
```

**Windows (Firefox):**
```batch
cd native-host
register_firefox.bat
```

### 3. Load Extension

**Chrome:**
1. Go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" → select the `extension` folder

**Firefox:**
1. Go to `about:debugging#/runtime/this-firefox`
2. Click "Load Temporary Add-on" → select `extension/manifest-firefox.json`

## Usage

1. **Visit a video site** (YouTube, Vimeo, etc.)
2. **Play a video** - the extension will detect the stream
3. **Look for "!" badge** on the extension icon
4. **Click the extension** → see detected stream URL
5. **Click "➕ Download"** → added to queue
6. **Monitor progress** in the queue or check logs

### Multiple Downloads

1. Start a download
2. Go to another tab with a different video
3. Click "🔄 Clear" to reset detection
4. Refresh the video page
5. Click "➕ Download" again
6. Both downloads run in parallel!

## Project Structure

```
ffmpeg-downloader/
├── extension/
│   ├── manifest.json        # Chrome MV3 manifest
│   ├── manifest-firefox.json # Firefox MV2 manifest
│   ├── background.js        # Service worker - intercepts requests
│   ├── popup.html           # UI layout
│   └── popup.js             # Queue management
├── native-host/
│   ├── host.py              # Python script that runs FFmpeg
│   ├── com.my_downloader.json    # Native messaging manifest (Chrome)
│   ├── com.my_downloader.firefox.json # Native messaging manifest (Firefox)
│   ├── requirements.txt     # Python dependencies
│   └── install_host.bat     # Windows installer
├── logs/
│   └── ffmpeg-download.log  # Download progress logs
└── .github/workflows/
    ├── ci.yml               # CI pipeline
    └── release.yml          # Auto-release on tags
```

## How It Works

### 1. Stream Detection (`background.js`)

The extension intercepts all web requests and checks for video URLs:

```javascript
const MEDIA_EXTENSIONS = ['.m3u8', '.mpd', '.mp4', '.flv', '.webm'];

chrome.webRequest.onBeforeRequest.addListener((details) => {
  if (MEDIA_EXTENSIONS.some(ext => details.url.includes(ext))) {
    // Save detected stream
    chrome.storage.local.set({ last_stream: details.url });
    setBadge("!");
  }
}, { urls: ["<all_urls>"] });
```

### 2. Native Messaging Protocol

Chrome ↔ Python communication uses a binary protocol:

```
┌──────────┬─────────────────────────┐
│ 4 bytes  │     JSON message        │
│ (length) │                         │
└──────────┴─────────────────────────┘
```

**Reading in Python:**
```python
raw_length = sys.stdin.buffer.read(4)
message_length = struct.unpack('@I', raw_length)[0]
message = sys.stdin.buffer.read(message_length).decode('utf-8')
return json.loads(message)
```

### 3. FFmpeg Download (`host.py`)

```python
ffmpeg_cmd = [
    'C:\\ffmpeg\\ffmpeg.exe',
    '-i', url,           # Input stream URL
    '-c', 'copy',        # Stream copy (no re-encoding)
    '-movflags', '+faststart',
    output_path
]
process = subprocess.Popen(ffmpeg_cmd, ...)
```

### 4. Progress Monitoring

The host monitors file size and logs progress every 5 seconds:

```
[INFO] FFmpeg started with PID: 12345
[PROGRESS] PID 12345: 15.32 MB downloaded | Speed: 24.51 Mbps | Elapsed: 5s
[PROGRESS] PID 12345: 45.67 MB downloaded | Speed: 48.56 Mbps | Elapsed: 10s
[COMPLETE] PID 12345: 156.78 MB | Total time: 32s | Avg speed: 39.19 Mbps
```

## Commands

| Command | Sent By | Action |
|---------|---------|--------|
| `{ url, filename }` | popup → host | Start FFmpeg download |
| `{ command: "kill", pid }` | popup → host | Stop download |
| `{ command: "get-progress", pid, filename }` | background → host | Check file size |

## Storage Structure

```javascript
// chrome.storage.local
{
  last_stream: "https://..../playlist.m3u8",
  downloads: [
    {
      pid: 12345,
      filename: "video.mp4",
      status: "downloading", // downloading | completed | error | stopped
      currentSize: 1234567,
      speedText: "2.5 MB/s"
    }
  ]
}
```

## Troubleshooting

### "Native host not found"
- Run `install_host.bat` as Administrator
- Check registry: `HKCU\Software\Google\Chrome\NativeMessagingHosts\com.my_downloader`

### "FFmpeg not found"
- Install FFmpeg and update path in `host.py` line ~196

### Stream not detected
- Refresh the video page
- Check if "!" badge appears
- Open DevTools → Network tab → filter by "m3u8" or "mp4"

### Check logs
```powershell
Get-Content "logs/ffmpeg-download.log" -Tail 50
```

## Development

### Run Tests
```bash
pytest tests/ -v
```

### Lint
```bash
flake8 native-host/host.py
```

### Create Release
```bash
git tag v1.0.0
git push origin v1.0.0
# GitHub Actions will create release automatically
```

## License

MIT
