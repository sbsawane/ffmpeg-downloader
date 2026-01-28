// Cross-browser compatibility (Chrome uses 'chrome', Firefox uses 'browser')
const API = typeof browser !== 'undefined' ? browser : chrome;
const IS_FIREFOX = typeof browser !== 'undefined';

// Listen for media files - expanded patterns
const MEDIA_EXTENSIONS = ['.m3u8', '.mpd', '.mp4', '.flv', '.webm', '.mkv', '.avi', '.mov'];
const MEDIA_PATTERNS = ['playlist', 'chunklist', 'master', 'index', 'manifest', 'stream', 'video', 'media'];

// Helper function for setting badge (works with both Chrome MV3 and Firefox MV2)
function setBadge(text) {
  try {
    if (IS_FIREFOX) {
      // Firefox MV2
      browser.browserAction.setBadgeText({ text: text });
    } else {
      // Chrome MV3
      chrome.action.setBadgeText({ text: text });
    }
  } catch (e) {
    console.log("Badge not supported:", e.message);
  }
}

// Cross-browser native messaging helper
// Firefox returns Promises, Chrome uses callbacks
function sendNativeMessage(hostName, message) {
  return new Promise((resolve, reject) => {
    if (IS_FIREFOX) {
      // Firefox: Promise-based API
      browser.runtime.sendNativeMessage(hostName, message)
        .then(response => resolve(response))
        .catch(error => reject(error));
    } else {
      // Chrome: Callback-based API
      chrome.runtime.sendNativeMessage(hostName, message, (response) => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
        } else {
          resolve(response);
        }
      });
    }
  });
}

// Initialize
try {
  // Clear storage on startup
  API.storage.local.remove('last_stream');
  setBadge("");
} catch (e) {
  console.log("Initialization error:", e.message);
}

// Monitor web requests for media files (Cross-browser compatible)
try {
  // Use API for cross-browser compatibility (Firefox uses browser.*, Chrome uses chrome.*)
  const webRequestAPI = typeof browser !== 'undefined' ? browser.webRequest : chrome.webRequest;
  
  webRequestAPI.onBeforeRequest.addListener(
    (details) => {
      const url = details.url.toLowerCase();
      const originalUrl = details.url;
      
      // Skip small segments and chunks
      if (url.includes('.m4s') || url.includes('.ts?') || url.match(/\/seg-\d+/) || url.includes('/chunk')) {
        return;
      }
      
      // Check for media extensions
      const hasMediaExt = MEDIA_EXTENSIONS.some(ext => url.includes(ext));
      
      // Check for media patterns in URL (for streams without clear extensions)
      const hasMediaPattern = MEDIA_PATTERNS.some(pattern => url.includes(pattern)) && 
                              (url.includes('m3u8') || url.includes('.mp4') || url.includes('video'));
      
      // Check content type header for video
      const isVideoType = details.type === 'media' || details.type === 'xmlhttprequest';
      
      if (hasMediaExt || (hasMediaPattern && isVideoType)) {
        console.log('[Stream Detected]', originalUrl);
        API.storage.local.set({ last_stream: originalUrl });
        setBadge("!");
      }
    },
    { urls: ["<all_urls>"] }
  );
} catch (e) {
  console.log("webRequest not available:", e.message);
}

// 3. Handle Download Messages and Kill Commands
API.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.command === "download") {
    console.log("Download request:", message);
    
    // Use cross-browser native messaging helper
    sendNativeMessage("com.my_downloader", { url: message.url, filename: message.filename })
      .then(response => {
        if (response && response.status === "success") {
          console.log("Download started successfully:", response);
          sendResponse({ 
            status: "started", 
            pid: response.pid, 
            filename: response.filename, 
            path: response.path 
          });
          
          // Start monitoring progress for this download
          if (response.pid) {
            startProgressMonitoring(response.pid, response.filename, response.path);
          }
        } else if (response && response.status === "error") {
          console.error("FFmpeg error:", response.message);
          sendResponse({ status: "error", error: response.message || "FFmpeg failed to start" });
        } else {
          console.warn("Unexpected response from native host:", response);
          sendResponse({ status: "error", error: "Invalid response from native host" });
        }
      })
      .catch(error => {
        const errorMsg = error.message || "Unknown native host error";
        console.error("Native Host Error:", errorMsg);
        sendResponse({ status: "error", error: errorMsg });
      });
    
    return true; // Keep message channel open for async response
  }
  
  if (message.command === "kill") {
    const pid = message.pid;
    if (pid) {
      sendNativeMessage("com.my_downloader", { command: "kill", pid: pid })
        .then(response => {
          console.log("Kill response:", response);
          sendResponse({ status: "killed" });
        })
        .catch(error => {
          console.error("Kill error:", error);
          sendResponse({ status: "error", error: error.message });
        });
      return true;
    }
  }
});

// Monitor progress for a specific download by checking file size
function startProgressMonitoring(pid, filename, path) {
  let lastSize = 0;
  let lastTime = Date.now();
  let stuckCount = 0;
  const maxStuckChecks = 60; // Consider complete after 30 seconds of no growth
  
  const progressInterval = setInterval(() => {
    // Check file size by sending get-progress command (cross-browser)
    sendNativeMessage("com.my_downloader", { command: "get-progress", pid: pid, filename: filename })
      .then(response => {
        API.storage.local.get(['downloads'], (result) => {
          const downloads = result.downloads || [];
          const download = downloads.find(d => d.pid === pid);
          
          if (!download || download.status !== 'downloading') {
            clearInterval(progressInterval);
            return;
          }
          
          if (response && response.status === "progress") {
            const currentSize = response.downloaded || 0;
            const now = Date.now();
            const timeDiff = (now - lastTime) / 1000;
            const sizeDiff = currentSize - lastSize;
            
            // Calculate speed
            let speedText = 'Calculating...';
            if (timeDiff > 0 && sizeDiff > 0) {
              const speedMBps = (sizeDiff / (1024 * 1024)) / timeDiff;
              speedText = `${speedMBps.toFixed(2)} MB/s`;
              stuckCount = 0;
            } else {
              stuckCount++;
            }
            
            // Update download in queue
            download.currentSize = currentSize;
            download.speedText = `${(currentSize / (1024*1024)).toFixed(2)} MB | ${speedText}`;
            
            lastSize = currentSize;
            lastTime = now;
            
            // Check if download might be complete (no growth for 30 seconds)
            if (stuckCount >= maxStuckChecks && currentSize > 0) {
              download.status = 'completed';
              download.finalSize = currentSize;
              clearInterval(progressInterval);
            }
            
            API.storage.local.set({ downloads: downloads });
          } else if (response && response.status === "error") {
            // Process might have finished - check if file exists with size
            stuckCount++;
            if (stuckCount >= maxStuckChecks) {
              if (lastSize > 0) {
                download.status = 'completed';
                download.finalSize = lastSize;
              } else {
                download.status = 'error';
                download.error = 'Download failed or file not found';
              }
              API.storage.local.set({ downloads: downloads });
              clearInterval(progressInterval);
            }
          }
        });
      })
      .catch(error => {
        console.log("Progress check failed:", error.message);
        stuckCount++;
        if (stuckCount >= maxStuckChecks) {
          clearInterval(progressInterval);
        }
      });
  }, 2000); // Check every 2 seconds
}