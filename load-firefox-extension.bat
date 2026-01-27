@echo off
REM Firefox Extension Loader Script
REM This script helps load the FFmpeg extension in Firefox for testing

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Firefox Extension Loader
echo FFmpeg Stream Downloader v1.1
echo ========================================
echo.

REM Check if Firefox is installed
if not exist "C:\Program Files\Mozilla Firefox\firefox.exe" (
    echo ERROR: Firefox not found at C:\Program Files\Mozilla Firefox\firefox.exe
    echo Please install Firefox first.
    pause
    exit /b 1
)

echo [1/3] Firefox found at: C:\Program Files\Mozilla Firefox\firefox.exe
echo.

REM Check if manifest file exists
set MANIFEST=F:\Projects\ffmpeg-downloader\extension\manifest-firefox.json
if not exist "%MANIFEST%" (
    echo ERROR: Manifest file not found at: %MANIFEST%
    echo Please ensure the project is at: F:\Projects\ffmpeg-downloader
    pause
    exit /b 1
)

echo [2/3] Manifest file found at: %MANIFEST%
echo.

echo [3/3] Opening Firefox with debugging enabled...
echo.
echo Instructions:
echo.
echo   1. Firefox will open to about:debugging page
echo   2. Click "This Firefox" in the left sidebar
echo   3. Click "Load Temporary Add-on" button
echo   4. Navigate to: %MANIFEST%
echo   5. Select the file and click "Open"
echo.
echo.

REM Open Firefox to about:debugging
start "" "C:\Program Files\Mozilla Firefox\firefox.exe" "about:debugging"

REM Wait a moment, then open file dialog hint
timeout /t 5 /nobreak

echo The manifest file path has been copied below for easy access:
echo.
echo %MANIFEST%
echo.
echo You can now proceed with loading the extension in Firefox.
echo Press any key to continue...
pause

echo.
echo After loading the extension:
echo   1. Visit a website with video content
echo   2. Play the video
echo   3. Look for the extension icon in the toolbar
echo   4. Click to see detected streams
echo.

pause
