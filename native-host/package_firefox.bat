@echo off
REM Create a Firefox extension package (.zip)

setlocal enabledelayedexpansion

set EXT_FOLDER=F:\Projects\ffmpeg-downloader\extension
set OUTPUT_ZIP=F:\Projects\ffmpeg-downloader\ffmpeg-downloader-firefox.zip
set TEMP_FOLDER=%TEMP%\ffmpeg_firefox_build

echo Creating Firefox extension package...

REM Clean up temp folder
if exist "%TEMP_FOLDER%" rmdir /s /q "%TEMP_FOLDER%"
mkdir "%TEMP_FOLDER%"

REM Copy files to temp folder (at root level for Firefox)
copy "%EXT_FOLDER%\manifest-firefox.json" "%TEMP_FOLDER%\manifest.json" >nul
copy "%EXT_FOLDER%\background.js" "%TEMP_FOLDER%\background.js" >nul
copy "%EXT_FOLDER%\popup.html" "%TEMP_FOLDER%\popup.html" >nul
copy "%EXT_FOLDER%\popup.js" "%TEMP_FOLDER%\popup.js" >nul

REM Remove old zip if it exists
if exist "%OUTPUT_ZIP%" del "%OUTPUT_ZIP%"

REM Create zip using PowerShell (proper structure)
powershell -Command "Compress-Archive -Path '%TEMP_FOLDER%\*' -DestinationPath '%OUTPUT_ZIP%' -Force"

REM Cleanup temp folder
rmdir /s /q "%TEMP_FOLDER%"

if exist "%OUTPUT_ZIP%" (
    echo.
    echo ✓ Firefox extension package created!
    echo Location: %OUTPUT_ZIP%
    echo.
    echo To install in Firefox:
    echo 1. Go to about:debugging
    echo 2. Click "Load Temporary Add-on"
    echo 3. Select: %OUTPUT_ZIP%
    echo.
) else (
    echo ERROR: Failed to create package!
)
pause
