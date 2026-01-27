# Installation and Usage Guide

## Browser Installation

### Chrome / Chromium (MV3)

1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer mode** (top right toggle)
3. Click **Load unpacked**
4. Select the `extension/` folder from this project
5. The FFmpeg icon should appear in your toolbar

### Firefox (MV2)

1. Open Firefox and go to `about:debugging`
2. Click **This Firefox** in the left panel
3. Click **Load Temporary Add-on**
4. Navigate to `extension/manifest-firefox.json` in this project
5. Select it and click Open
6. The FFmpeg icon should appear in your toolbar

## Usage

### How to Download a Stream

1. **Navigate** to a website with video content (e.g., YouTube, Twitch, etc.)
2. **Play the video** - the extension will detect the stream
3. **Look for the badge** - when a stream is detected, the extension icon will show a `!` badge
4. **Click the extension icon** to open the popup
5. **The stream URL** will be auto-populated in the "Detected Stream" field
6. **(Optional)** Change the filename if desired
7. **Click "Start Download"** button
8. **Watch the progress bar** - it will show download percentage and MB/MB
9. **Check your Downloads folder** for the file once complete

### Monitor Progress

- **Spinner animation** - shows download is in progress
- **Progress bar** - fills as file downloads
- **Percentage** - shows completion percentage
- **MB counter** - shows downloaded/total megabytes

### Stop a Download

- Click the **"Stop Download"** button to cancel an active download
- The file will be saved with whatever was downloaded so far

## Troubleshooting

### "Error: Native host not found"
**Solution**: Ensure the native host is properly installed:
```
cd native-host
python install_host.bat
```

### No streams detected
**Solution**: Some websites block stream detection. Try:
- Playing video directly from HTML5 `<video>` tags
- Checking if the video is embedded in an iframe (extension may not detect cross-origin streams)
- Looking for `.m3u8` or `.mpd` URLs in the network tab of Developer Tools

### File not created or 0 bytes
**Solution**: This means the FFmpeg connection failed. Check:
1. FFmpeg is installed: `C:\ffmpeg\ffmpeg.exe --version`
2. The URL is valid and accessible
3. Logs at `logs/ffmpeg-download.log` for errors
4. Check Windows Defender hasn't blocked native messaging

### "Native messaging host error" 
**Solution**: The Python native host crashed. Check the logs:
- Open `logs/ffmpeg-download.log`
- Look for `[ERROR]` entries
- Common issues:
  - FFmpeg URL requires authentication
  - Stream URL has expired
  - Insufficient disk space

## What This Extension Does

1. **Stream Detection** - Monitors network requests for media files (.m3u8, .mp4, .mpd, .flv)
2. **Native Messaging** - Communicates with a Python script running FFmpeg
3. **Download** - Uses FFmpeg to download the stream to your Downloads folder
4. **Progress Tracking** - Polls the native host for real-time download progress
5. **Process Control** - Can stop downloads gracefully or forcefully

## File Locations

- **Downloads**: `C:\Users\[Username]\Downloads\`
- **Logs**: `F:\Projects\ffmpeg-downloader\logs\ffmpeg-download.log`
- **Config**: `F:\Projects\ffmpeg-downloader\native-host\com.my_downloader.json`
