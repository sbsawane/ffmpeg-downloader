# 🦊 Testing FFmpeg Extension in Firefox

## Quick Start (3 Steps)

### Step 1: Open Firefox Debugging Page
```
In Firefox address bar, type: about:debugging
Press Enter
```

### Step 2: Load the Extension
```
1. Click "This Firefox" in left sidebar
2. Click "Load Temporary Add-on" button
3. Select file: F:\Projects\ffmpeg-downloader\extension\manifest-firefox.json
4. Click "Open"
```

### Step 3: Test It
```
1. Visit any website with video
2. Play the video
3. Click extension icon (look for "!")
4. Click "Start Download"
```

---

## 📍 File Location for Step 2

When Firefox asks you to select the add-on file, navigate to:

```
F:\Projects\ffmpeg-downloader\extension\manifest-firefox.json
```

The full path breakdown:
- Drive: `F:\`
- Folder: `Projects\`
- Folder: `ffmpeg-downloader\`
- Folder: `extension\`
- File: `manifest-firefox.json` ← **Select this file**

---

## ✅ What Should Happen

**After loading:**
- Extension appears in the list on about:debugging
- No errors shown
- Status shows "Temporary"

**When you visit a video site:**
- Extension icon appears in toolbar (top right)
- When video plays, icon shows "!" badge
- Clicking icon opens popup with auto-filled URL

**When you download:**
- Progress bar animates
- Percentage and MB shown
- File appears in Downloads folder

---

## 🐛 If Something Goes Wrong

### "Manifest file not found"
Make sure you're selecting:
```
F:\Projects\ffmpeg-downloader\extension\manifest-firefox.json
```
(NOT the Chrome manifest.json)

### "Native host error"
1. Restart Firefox
2. Check: `F:\Projects\ffmpeg-downloader\logs\ffmpeg-download.log`
3. Run: `python F:\Projects\ffmpeg-downloader\native-host\install_host.bat`

### No "!" badge appears
- Try a different video website
- Check Developer Tools (F12) → Network tab for .mp4/.m3u8 URLs
- Some websites block stream detection

### Download fails immediately
- Check the logs file
- Try with a public video URL (not DRM-protected)
- Look for error messages in about:debugging console

---

## 📚 Additional Resources

- **Full guide**: See `FIREFOX_GUIDE.md` for detailed troubleshooting
- **Browser compatibility**: Both Chrome (MV3) and Firefox (MV2) supported
- **Logs location**: `F:\Projects\ffmpeg-downloader\logs\ffmpeg-download.log`
- **Launcher script**: Run `load-firefox-extension.bat` for guided loading

---

## 🎯 Test Checklist

- [ ] Extension loads without errors
- [ ] No errors on about:debugging page
- [ ] Icon appears in toolbar
- [ ] Icon shows "!" badge when video plays
- [ ] Clicking icon opens popup
- [ ] URL auto-fills in popup
- [ ] "Start Download" button works
- [ ] Progress bar appears
- [ ] Percentage shows correctly
- [ ] MB counter shows correctly
- [ ] File created in Downloads
- [ ] File has reasonable size (not 0 bytes)
- [ ] "Stop Download" button works

---

**Firefox is ready for testing!** 🚀

Follow the 3 quick steps above and you're good to go.
