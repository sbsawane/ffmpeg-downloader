@echo off
REM Register native host for Firefox
REM Note: Replace "ffmpeg-downloader@example.com" with your actual Firefox extension ID

setlocal enabledelayedexpansion
set MANIFEST_PATH=%~dp0com.my_downloader.firefox.json
set REGISTRY_PATH=HKCU\Software\Mozilla\NativeMessagingHosts\com.my_downloader

echo Registering Firefox native host...
echo Manifest: !MANIFEST_PATH!
echo Registry: !REGISTRY_PATH!

reg add "!REGISTRY_PATH!" /ve /t REG_SZ /d "!MANIFEST_PATH!" /f

if %errorlevel% equ 0 (
    echo.
    echo ✓ Firefox native host registered successfully!
    echo.
    echo IMPORTANT: You must also:
    echo 1. Install the extension in Firefox
    echo 2. Update the extension ID in com.my_downloader.firefox.json
    echo    - Go to about:debugging in Firefox
    echo    - Find your extension and copy its UUID
    echo    - Replace "ffmpeg-downloader@example.com" with the UUID
) else (
    echo ERROR: Failed to register! You may need to run as Administrator.
)
pause
