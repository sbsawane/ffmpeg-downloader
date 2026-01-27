# Quick Start Guide

## Prerequisites

✅ **Already Done:**
- FFmpeg installed at `C:\ffmpeg\ffmpeg.exe`
- Python host configured at `F:\Projects\ffmpeg-downloader\native-host\host.py`
- Native messaging registry keys installed

## Step 1: Load Extension in Chrome

```
1. Open: chrome://extensions/
2. Enable: Developer mode (top right)
3. Click: Load unpacked
4. Select: F:\Projects\ffmpeg-downloader\extension\
5. Confirm: Extension appears with FFmpeg icon
```

## Step 2: Load Extension in Firefox (Optional)

```
1. Open: about:debugging
2. Click: This Firefox
3. Click: Load Temporary Add-on
4. Select: F:\Projects\ffmpeg-downloader\extension\manifest-firefox.json
5. Confirm: Extension appears with FFmpeg icon
```

## Step 3: Test with a Video Website

```
1. Visit a website with embedded video:
   - YouTube
   - Vimeo
   - Any site with <video> tag or .m3u8 stream
2. Play the video
3. Look for the extension icon in toolbar
4. You should see a "!" badge appear
```

## Step 4: Download a Stream

```
1. Click the extension icon
2. Popup opens with the detected stream URL
3. (Optional) Change the filename
4. Click "Start Download"
5. Watch the progress bar fill up
```

## Step 5: Monitor Download

- The popup shows:
  - Spinner animation while downloading
  - Progress bar percentage
  - Current MB / Total MB
  - PID of the process

## Step 6: Check Result

```
Location: C:\Users\sande\Downloads\
Your downloaded file will be here
```

## Troubleshooting

### Problem: No "!" badge appears
**Possible causes:**
- Website doesn't serve videos directly (JavaScript rendered)
- Video is DRM protected
- Stream URL is in JavaScript, not network request

**Solution:**
- Open Developer Tools (F12)
- Go to Network tab
- Look for .m3u8 or .mp4 URLs
- Copy and paste directly into extension

### Problem: "Native host not found" error
**Solution:**
1. Make sure `start_host.bat` exists at: `F:\Projects\ffmpeg-downloader\native-host\start_host.bat`
2. Run: `python F:\Projects\ffmpeg-downloader\native-host\install_host.bat`
3. Restart the browser
4. Try again

### Problem: Download shows 0% or fails immediately
**Possible causes:**
- URL has expired (time-limited download links)
- Stream requires authentication/cookies
- FFmpeg can't access the URL

**Solution:**
1. Check the logs: `F:\Projects\ffmpeg-downloader\logs\ffmpeg-download.log`
2. Look for `[ERROR]` lines
3. Try with a different video source
4. Verify the URL works in your browser

### Problem: Extension icon has yellow warning triangle
**Cause:** Usually means native host communication issue

**Solution:**
1. Check Windows Event Viewer for errors
2. Verify `com.my_downloader.json` is readable
3. Verify `start_host.bat` can execute Python
4. Run: `python -u C:\Python312\python.exe F:\Projects\ffmpeg-downloader\native-host\host.py` to test manually

## Test Video URLs

Use these to test (if accessible):
- YouTube: Any public video (embed stream)
- Vimeo: https://vimeo.com/ (if they serve HLS)
- MDN Example: https://commondatastorage.googleapis.com/gtv-videos-library/sample/ElephantsDream.mp4

## Debug Mode

To see detailed logs:
1. Open DevTools: F12 in browser
2. Go to Console tab
3. You'll see all download progress and errors
4. Also check: `F:\Projects\ffmpeg-downloader\logs\ffmpeg-download.log`

## What to Expect

- **Fast streams** (direct MP4): Downloads at full network speed
- **HLS/DASH streams** (.m3u8/.mpd): FFmpeg re-encodes, may be slower
- **Progress updates**: Every 500ms
- **File location**: Always in Downloads folder

## Success Indicators

✅ Extension icon appears in toolbar
✅ Badge shows "!" when visiting video website  
✅ URL auto-fills in popup
✅ Download button is clickable
✅ Progress bar animates
✅ File appears in Downloads folder

## Next: Real Testing

Try these in order:
1. Test with HTML5 `<video>` element (easiest)
2. Test with YouTube (medium - may have restrictions)
3. Test with custom/private video (advanced)

All the infrastructure is ready - just need a video to download!
