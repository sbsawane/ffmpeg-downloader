# 🦊 Firefox Testing - Quick Reference Card

## The Essentials

### File to Load
```
F:\Projects\ffmpeg-downloader\extension\manifest-firefox.json
```

### Steps (5 Easy Steps)
```
1. Firefox address bar → type: about:debugging
2. Left sidebar → click: This Firefox
3. Click button: Load Temporary Add-on
4. Select file: manifest-firefox.json (see path above)
5. Click: Open
```

### Expected Result
✓ Extension appears in the list  
✓ No errors shown  
✓ Status shows "Temporary"  
✓ Icon appears in toolbar  

---

## Testing After Loading

### Step A: Visit a Video Website
- Go to any site with video (YouTube, Vimeo, etc.)
- Play the video

### Step B: Check for Badge
- Look at extension icon in toolbar
- Should see "!" badge

### Step C: Click Extension Icon
- Popup opens
- Stream URL auto-fills
- Filename field shows "output.mp4"

### Step D: Download
- Click "Start Download"
- Watch spinner
- Progress bar appears
- Shows percentage and MB

### Step E: Verify
- Download completes
- File appears in Downloads
- File is not 0 bytes
- File plays in media player

---

## Troubleshooting

### "File not found" when loading
→ Make sure you selected: **manifest-firefox.json** (not manifest.json)

### No "!" badge appears
→ Try different video website, some don't serve detectable streams

### "Native host error"
→ Run: `python F:\Projects\ffmpeg-downloader\native-host\install_host.bat`
→ Then restart Firefox

### Download shows 0% / fails
→ Check: `F:\Projects\ffmpeg-downloader\logs\ffmpeg-download.log` for errors

### Icon doesn't appear
→ Click Extensions menu (puzzle icon) and look for FFmpeg Downloader

---

## Documentation

- **Quick tips**: This card (you're reading it!)
- **Details**: `FIREFOX_TEST.md`
- **Troubleshooting**: `FIREFOX_GUIDE.md`
- **Full checklist**: `FIREFOX_TESTING_CHECKLIST.md`

---

## Key Files

| File | Purpose |
|------|---------|
| manifest-firefox.json | Extension configuration |
| background.js | Stream detection & messaging |
| popup.html | User interface |
| popup.js | Download control |
| host.py | FFmpeg communication |

---

## System Requirements

✓ Firefox browser  
✓ Windows 10/11  
✓ FFmpeg at `C:\ffmpeg\ffmpeg.exe`  
✓ Python 3.12+  
✓ ~500MB disk space  

---

## Expected Performance

- **Detection**: Stream appears within 2-5 seconds
- **Download start**: ~1-2 seconds after click
- **Progress updates**: Every 500ms
- **Speed**: Limited only by network/server

---

## Success Checklist

- [ ] Extension loads on about:debugging
- [ ] Icon appears in toolbar
- [ ] Badge shows on video sites
- [ ] URL auto-fills in popup
- [ ] Download starts
- [ ] Progress bar animates
- [ ] File created in Downloads
- [ ] File has reasonable size (>1MB for video)

---

**Done? You're ready to test! 🚀**

Any issues? Check the full guides:
- `FIREFOX_GUIDE.md` - Complete help
- `FIREFOX_TESTING_CHECKLIST.md` - Detailed verification
