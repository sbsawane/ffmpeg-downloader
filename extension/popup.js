// Cross-browser compatibility
const API = typeof browser !== 'undefined' ? browser : chrome;

let refreshInterval = null;

document.addEventListener('DOMContentLoaded', () => {
  const urlInput = document.getElementById('urlInput');
  const filenameInput = document.getElementById('filename');
  const downloadBtn = document.getElementById('downloadBtn');
  const clearBtn = document.getElementById('clearBtn');
  const clearCompletedBtn = document.getElementById('clearCompletedBtn');
  const statusMsg = document.getElementById('statusMsg');
  const downloadQueue = document.getElementById('downloadQueue');
  const activeCount = document.getElementById('activeCount');
  const emptyQueue = document.getElementById('emptyQueue');
  
  // Load last detected stream
  API.storage.local.get(['last_stream'], (result) => {
    if (result.last_stream) {
      urlInput.value = result.last_stream;
    }
  });
  
  // Load and render queue
  function loadQueue() {
    API.storage.local.get(['downloads'], (result) => {
      const downloads = result.downloads || [];
      renderQueue(downloads);
    });
  }
  
  // Render download queue
  function renderQueue(downloads) {
    if (downloads.length === 0) {
      downloadQueue.innerHTML = '<div id="emptyQueue">No downloads yet</div>';
      activeCount.textContent = '0';
      return;
    }
    
    const activeDownloads = downloads.filter(d => d.status === 'downloading').length;
    activeCount.textContent = activeDownloads;
    
    downloadQueue.innerHTML = downloads.map((d, index) => `
      <div class="download-item ${d.status}" data-index="${index}">
        <div class="download-filename">${d.filename}</div>
        <div class="download-status">${getStatusText(d)}</div>
        ${d.status === 'downloading' ? `
          <div class="download-progress">
            <div class="download-progress-fill" style="width: ${d.progress || 0}%"></div>
          </div>
          <div class="download-speed">${d.speedText || 'Starting...'}</div>
        ` : ''}
        <div class="download-actions">
          ${d.status === 'downloading' ? 
            `<button class="stop-btn" data-pid="${d.pid}">⏹ Stop</button>` : 
            `<button class="remove-btn" data-index="${index}">✕</button>`
          }
        </div>
      </div>
    `).join('');
    
    // Add event listeners for stop/remove buttons
    downloadQueue.querySelectorAll('.stop-btn').forEach(btn => {
      btn.addEventListener('click', () => stopDownload(parseInt(btn.dataset.pid)));
    });
    
    downloadQueue.querySelectorAll('.remove-btn').forEach(btn => {
      btn.addEventListener('click', () => removeDownload(parseInt(btn.dataset.index)));
    });
  }
  
  function getStatusText(d) {
    switch(d.status) {
      case 'downloading': 
        return `⏳ Downloading... PID: ${d.pid}`;
      case 'completed': 
        return `✅ Completed - ${formatSize(d.finalSize || 0)}`;
      case 'error': 
        return `❌ Error: ${d.error || 'Unknown'}`;
      case 'stopped': 
        return `⏹ Stopped`;
      default: 
        return d.status;
    }
  }
  
  function formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
  }
  
  // Start a new download
  downloadBtn.addEventListener('click', () => {
    const url = urlInput.value;
    let filename = filenameInput.value || 'output.mp4';
    
    if (!url) {
      statusMsg.innerHTML = '⚠️ No stream detected. Refresh the video page.';
      return;
    }
    
    statusMsg.innerHTML = '⏳ Starting download...';
    
    API.runtime.sendMessage({ command: "download", url: url, filename: filename }, (response) => {
      if (response && response.status === "started") {
        const newDownload = {
          pid: response.pid,
          filename: response.filename || filename,
          path: response.path,
          url: url,
          status: 'downloading',
          progress: 0,
          startTime: Date.now()
        };
        
        // Add to queue
        API.storage.local.get(['downloads'], (result) => {
          const downloads = result.downloads || [];
          downloads.unshift(newDownload); // Add to top
          API.storage.local.set({ downloads: downloads }, () => {
            loadQueue();
            statusMsg.innerHTML = '✅ Download added to queue!';
            
            // Clear the detected stream so user can add another
            API.storage.local.remove(['last_stream']);
            urlInput.value = '';
            filenameInput.value = 'output.mp4';
            
            // Clear badge
            try {
              if (typeof browser !== 'undefined') {
                browser.browserAction.setBadgeText({ text: '' });
              } else {
                chrome.action.setBadgeText({ text: '' });
              }
            } catch(e) {}
          });
        });
      } else {
        const errorMsg = response?.error || 'Unknown error';
        statusMsg.innerHTML = `❌ Error: ${errorMsg}`;
      }
    });
  });
  
  // Stop a download
  function stopDownload(pid) {
    API.runtime.sendMessage({ command: "kill", pid: pid }, (response) => {
      API.storage.local.get(['downloads'], (result) => {
        const downloads = result.downloads || [];
        const download = downloads.find(d => d.pid === pid);
        if (download) {
          download.status = 'stopped';
        }
        API.storage.local.set({ downloads: downloads }, loadQueue);
      });
    });
  }
  
  // Remove a download from queue
  function removeDownload(index) {
    API.storage.local.get(['downloads'], (result) => {
      const downloads = result.downloads || [];
      downloads.splice(index, 1);
      API.storage.local.set({ downloads: downloads }, loadQueue);
    });
  }
  
  // Clear completed downloads
  clearCompletedBtn.addEventListener('click', () => {
    API.storage.local.get(['downloads'], (result) => {
      const downloads = (result.downloads || []).filter(d => d.status === 'downloading');
      API.storage.local.set({ downloads: downloads }, loadQueue);
    });
  });
  
  // Clear detected stream
  clearBtn.addEventListener('click', () => {
    API.storage.local.remove(['last_stream'], () => {
      urlInput.value = '';
      urlInput.placeholder = 'Cleared! Refresh the video page...';
      statusMsg.innerHTML = '🔄 Cleared. Refresh video page to detect new stream.';
      
      try {
        if (typeof browser !== 'undefined') {
          browser.browserAction.setBadgeText({ text: '' });
        } else {
          chrome.action.setBadgeText({ text: '' });
        }
      } catch(e) {}
      
      setTimeout(() => { statusMsg.innerHTML = ''; }, 3000);
    });
  });
  
  // Initial load
  loadQueue();
  
  // Refresh queue every 2 seconds to show progress updates
  refreshInterval = setInterval(loadQueue, 2000);
});

// Clean up on popup close
window.addEventListener('unload', () => {
  if (refreshInterval) clearInterval(refreshInterval);
});