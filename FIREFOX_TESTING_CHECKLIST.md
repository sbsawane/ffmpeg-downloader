# Firefox Testing Checklist

## Pre-Testing Setup

- [x] Firefox installed at `C:\Program Files\Mozilla Firefox\firefox.exe`
- [x] FFmpeg extension manifest created: `extension/manifest-firefox.json`
- [x] Native host configured and installed
- [x] Python host working on Windows
- [x] FFmpeg available at `C:\ffmpeg\ffmpeg.exe`

## Loading the Extension

### Opening about:debugging
- [ ] Firefox opens successfully
- [ ] Address bar accepts: `about:debugging`
- [ ] about:debugging page loads without errors

### Extension Loading
- [ ] "This Firefox" option visible in sidebar
- [ ] "Load Temporary Add-on" button clickable
- [ ] File browser opens when clicked
- [ ] Can navigate to `F:\Projects\ffmpeg-downloader\extension\`
- [ ] `manifest-firefox.json` file is selectable
- [ ] File selection succeeds without error

### Extension Appearance
- [ ] Extension appears in about:debugging list
- [ ] Name shows: "FFmpeg Stream Downloader"
- [ ] Version shows: "1.1"
- [ ] Status shows: "Temporary"
- [ ] Extension ID: `{5c82a32a-c068-486a-86ca-41e05f7a72b0}`
- [ ] No error messages displayed
- [ ] No warnings shown

### Toolbar Icon
- [ ] Icon appears in Firefox toolbar (top right area)
- [ ] Icon is clickable
- [ ] Icon appearance is consistent

## Stream Detection Testing

### Test with HTML5 Video
1. [ ] Visit a website with `<video>` element
2. [ ] Play the video
3. [ ] Look for "!" badge on extension icon
4. [ ] Badge appears within 2-5 seconds
5. [ ] Badge indicates stream detected

### Test with MP4 Links
1. [ ] Visit a page with direct `.mp4` links
2. [ ] Click/play the video
3. [ ] Extension detects it
4. [ ] Badge shows "!"

### Test with HLS/DASH Streams (if available)
1. [ ] Visit site with `.m3u8` or `.mpd` stream
2. [ ] Play the video
3. [ ] Extension detects the stream
4. [ ] Badge shows "!"

## Popup Functionality

### Opening Popup
- [ ] Clicking extension icon opens popup
- [ ] Popup displays without JavaScript errors
- [ ] Popup size is reasonable (not tiny or huge)
- [ ] UI elements are visible and readable

### Auto-Fill URL
- [ ] Detected stream URL appears in "Detected Stream" field
- [ ] URL is complete and correct
- [ ] URL is not truncated
- [ ] URL field is read-only (as expected)

### Filename Input
- [ ] "Save As" field is editable
- [ ] Can type custom filename
- [ ] Default value is "output.mp4"
- [ ] Special characters handled correctly

### Buttons
- [ ] "Start Download" button is visible
- [ ] Button text is clear and readable
- [ ] Button is clickable (mouse over shows cursor change)
- [ ] "Stop Download" button not visible yet (correct)

### Initial Status
- [ ] No error messages
- [ ] Progress bar is hidden (correct)
- [ ] Spinner is hidden (correct)
- [ ] Status message area is empty (correct)

## Download Functionality

### Starting Download
- [ ] Click "Start Download" button
- [ ] Button becomes disabled or changes appearance
- [ ] Status text changes to "⏳ Starting download..."
- [ ] No errors appear

### Download Progress
- [ ] Spinner animation appears (rotating circle)
- [ ] Spinner is visible and animated smoothly
- [ ] Progress bar appears (empty initially)
- [ ] Progress info box appears

### Progress Display
- [ ] Percentage appears in progress info (e.g., "0%")
- [ ] MB counter appears (e.g., "0.00 MB / 0.00 MB")
- [ ] Values update every ~500ms
- [ ] Percentage increases from 0 to 100
- [ ] MB counter shows increasing values

### UI Changes During Download
- [ ] "Start Download" button changes to "Stop Download"
- [ ] Stop button is red/different color
- [ ] Stop button is clickable
- [ ] Filename field becomes read-only
- [ ] URL field remains read-only

### Download Completion
- [ ] Progress bar reaches 100%
- [ ] Percentage shows "100%"
- [ ] Status updates (checkmark appears)
- [ ] File size seems reasonable (not 0 MB)
- [ ] After 3 seconds, UI resets

### File Creation
- [ ] File appears in `C:\Users\sande\Downloads\`
- [ ] Filename matches what was entered
- [ ] File size is larger than 0 bytes
- [ ] File is actually an MP4 (or appropriate format)
- [ ] File can be played in media player

## Stop/Pause Testing

### Stopping Mid-Download
1. [ ] Start a download
2. [ ] Wait for progress to show (not at 0%)
3. [ ] Click "Stop Download" button
4. [ ] Button text changes to "⏳ Stopping..."
5. [ ] Status shows stopping message
6. [ ] After ~1 second, process terminates
7. [ ] File is created with partial data

### Reset After Stop
- [ ] UI resets to initial state
- [ ] "Start Download" button reappears
- [ ] "Stop Download" button hidden
- [ ] Spinner stops animating
- [ ] Progress bar hidden
- [ ] Status message appears for 3 seconds then clears

## Error Handling

### Invalid URL
1. [ ] Manually enter an invalid URL
2. [ ] Click "Start Download"
3. [ ] Error appears quickly (not hanging)
4. [ ] Error message is helpful
5. [ ] "Start Download" button reappears

### Network Error
1. [ ] Try to download from non-existent server
2. [ ] Download fails gracefully (not frozen)
3. [ ] Error message shows (not generic)
4. [ ] UI resets properly

### Native Host Issues
1. [ ] If native host not responding
2. [ ] Error message appears: "Native host error" or similar
3. [ ] Error is specific and actionable
4. [ ] Extension recovers when host is available

## Console Logging

### DevTools Console (F12)
- [ ] Open Firefox DevTools (F12)
- [ ] Go to Console tab
- [ ] No JavaScript errors (red X's)
- [ ] Extension messages visible (if enabled)
- [ ] Download progress logged
- [ ] Completion logged

### Browser Console for Extensions
- [ ] about:debugging shows any extension errors
- [ ] No warnings about permissions
- [ ] No warnings about deprecated APIs
- [ ] Native messaging appears connected

## State Persistence

### Close and Reopen Popup
1. [ ] Start a download
2. [ ] Close the popup (click elsewhere)
3. [ ] Click extension icon again
4. [ ] Popup reopens
5. [ ] Download is still in progress
6. [ ] Progress is visible
7. [ ] Stop button appears

### Close and Reopen Firefox
1. [ ] Start extension (don't complete download)
2. [ ] Close Firefox (force quit is okay)
3. [ ] Reopen Firefox
4. [ ] Extension is still loaded (remembers temporary state)
5. [ ] Can continue testing

## Comparative Testing

### Chrome vs Firefox Differences
- [ ] Both detect streams the same way
- [ ] UI looks similar (allowing for browser differences)
- [ ] Download speed similar
- [ ] Progress tracking similar
- [ ] Error handling similar

## Performance

### Memory Usage
- [ ] Extension doesn't noticeably increase memory
- [ ] No memory leaks during long download
- [ ] Multiple downloads work without slowdown

### CPU Usage
- [ ] Download doesn't max out CPU
- [ ] Progress updates smooth (not jittery)
- [ ] No fan noise from laptop

### Network Bandwidth
- [ ] Download uses available bandwidth efficiently
- [ ] Speed is limited only by network/server
- [ ] Not artificially throttled

## Cross-Website Testing

Test extension on multiple sites:
- [ ] YouTube (if allows detection)
- [ ] Vimeo
- [ ] Generic HTML5 video player
- [ ] Streaming site (with accessible content)
- [ ] News website with video
- [ ] Social media platform with video

## Final Verification

- [ ] Extension works reliably
- [ ] No crashes or freezes
- [ ] Download produces usable files
- [ ] Progress tracking is accurate
- [ ] Error messages are helpful
- [ ] UI is responsive
- [ ] No Firefox warnings
- [ ] Performance is acceptable

## Notes & Observations

```
Use this space to record:
- Issues encountered
- Browser-specific behaviors
- Download speeds observed
- File sizes downloaded
- Any anomalies or unexpected behavior
```

---

## Summary

**Overall Status:** [ ] PASS [ ] FAIL [ ] PARTIAL

**Works:**
- [ ] Stream detection
- [ ] Download initiation
- [ ] Progress tracking
- [ ] File creation
- [ ] Stop functionality
- [ ] Error handling

**Issues Found:**
(List any issues discovered)

**Recommendations:**
(Suggestions for improvements)

---

**Date Tested:** _______________
**Tester:** ____________________
**Firefox Version:** ____________
**Notes:** ______________________
