# Firefox Extension Loading Guide

## Quick Steps

### Step 1: Open about:debugging
1. Open Firefox (should be launching now)
2. In the address bar, type: `about:debugging`
3. Press Enter

### Step 2: Navigate to This Firefox
- You'll see a sidebar on the left
- Click on **"This Firefox"**

### Step 3: Load Temporary Add-on
- Click the **"Load Temporary Add-on"** button
- A file browser will open

### Step 4: Select the Manifest File
Navigate to: `F:\Projects\ffmpeg-downloader\extension\manifest-firefox.json`

The path structure:
```
F:\
└── Projects\
    └── ffmpeg-downloader\
        └── extension\
            └── manifest-firefox.json  ← Select this file
```

### Step 5: Confirm Loading
- Click **"Open"** button
- You should see the extension appear in the list with status "Temporary"

## What You Should See

✓ Extension name: "FFmpeg Stream Downloader"
✓ Extension ID: {5c82a32a-c068-486a-86ca-41e05f7a72b0}
✓ Status: "Temporary" (for this session only)
✓ Icon appears in toolbar with "Add-ons" label

## Test the Extension

1. **Close the about:debugging tab** (keep Firefox open)
2. **Visit a website with video** (e.g., any video page)
3. **Play the video** - the extension will detect the stream
4. **Look for the extension icon in the toolbar** (top right area)
5. **Click the icon** to open the popup
6. **The detected stream URL should appear** in the "Detected Stream" field

## Troubleshooting

### Extension doesn't load
- Make sure you selected the correct `manifest-firefox.json` file
- Check the `manifest-firefox.json` is valid JSON
- Look for error messages in about:debugging page

### No icon appears in toolbar
- The icon may be in the Extensions menu (puzzle piece icon)
- Click the Extensions menu and pin the extension
- Alternatively, look in the "Add-ons" area

### Stream not detected
- Try visiting a different video website
- Check if the video is served directly (not JavaScript-rendered)
- Open DevTools (F12) → Network tab and look for .m3u8 or .mp4 URLs

### "Native host not found" error
- Make sure the native host is installed:
  ```
  cd F:\Projects\ffmpeg-downloader\native-host
  python install_host.bat
  ```
- Restart Firefox after installing the native host

## Test Video Websites

Try these sites for stream detection:
- HTML5 video pages (with `<video>` tag)
- Any site with direct MP4 video
- Sites with HLS streams (.m3u8)

## Features to Test

1. **Stream Detection**
   - [ ] Badge shows "!" when stream detected
   - [ ] URL auto-fills in popup
   - [ ] Filename is customizable

2. **Download**
   - [ ] "Start Download" button works
   - [ ] Spinner animation appears
   - [ ] Progress bar shows

3. **Progress Monitoring**
   - [ ] Progress bar fills from 0-100%
   - [ ] Percentage displayed
   - [ ] MB counter shows downloaded/total

4. **Stop Function**
   - [ ] "Stop Download" button appears during download
   - [ ] Clicking it stops the process
   - [ ] UI resets after stop

5. **File Creation**
   - [ ] Downloaded file appears in: `C:\Users\sande\Downloads\`
   - [ ] File has correct name
   - [ ] File size is reasonable (not 0 bytes)

## Expected Behavior

### When Extension Loads
- No errors on about:debugging page
- Extension appears with name and icon
- Status shows "Temporary"

### When Playing Video
- Extension icon shows "!" badge (if stream is detected)
- Clicking opens popup with auto-filled URL

### When Downloading
- Popup shows status: "⏳ Starting download..."
- Spinner animation begins
- After ~2-5 seconds: Progress bar appears
- Percentage and MB counter appear
- "Stop Download" button replaces "Start Download"

### When Download Completes
- Progress bar reaches 100%
- Status updates to "✓ Download completed"
- File appears in Downloads folder
- After 3 seconds, UI resets for next download

## Debug Information

If something goes wrong, check:
1. **Firefox Console**: F12 → Console tab
   - Look for error messages in red
   - Look for [INFO] logs from the extension

2. **about:debugging**
   - Shows any extension errors
   - Shows native host connection status

3. **Windows Logs**: F:\Projects\ffmpeg-downloader\logs\ffmpeg-download.log
   - Shows FFmpeg output
   - Shows native host errors
   - Shows all [INFO], [ERROR], [SUCCESS] messages

## Next Steps After Loading

1. **Test stream detection** on a video website
2. **Verify auto-fill** of stream URL
3. **Start a download** and monitor progress
4. **Check Downloads folder** for the file
5. **Check logs** to see FFmpeg output
6. **Report any issues** with error messages from console

---

**Ready to test Firefox! Follow the steps above to load the extension.**
