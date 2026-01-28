@echo off
REM Package extension for distribution
REM Creates ZIP files for Chrome and Firefox

echo ================================================
echo   FFmpeg Stream Downloader - Packager
echo ================================================
echo.

REM Create dist folder
if not exist "dist" mkdir "dist"

REM Get current date for filename
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /format:list') do set datetime=%%I
set VERSION=1.1
set DATESTAMP=%datetime:~0,8%

echo [1/3] Packaging Chrome extension...
if exist "dist\chrome-extension.zip" del "dist\chrome-extension.zip"
powershell -Command "Compress-Archive -Path 'extension\manifest.json','extension\background.js','extension\popup.html','extension\popup.js' -DestinationPath 'dist\chrome-extension.zip' -Force"
echo       Created: dist\chrome-extension.zip

echo.
echo [2/3] Building Firefox extension...
if exist "build\firefox" rmdir /s /q "build\firefox"
mkdir "build\firefox"
copy "extension\background.js" "build\firefox\" >nul
copy "extension\popup.html" "build\firefox\" >nul
copy "extension\popup.js" "build\firefox\" >nul
copy "extension\manifest-firefox.json" "build\firefox\manifest.json" >nul

echo [3/3] Packaging Firefox extension...
if exist "dist\firefox-extension.zip" del "dist\firefox-extension.zip"
powershell -Command "Compress-Archive -Path 'build\firefox\*' -DestinationPath 'dist\firefox-extension.zip' -Force"
echo       Created: dist\firefox-extension.zip

echo.
echo ================================================
echo   Packages created in 'dist' folder:
echo ================================================
echo.
echo   Chrome:  dist\chrome-extension.zip
echo   Firefox: dist\firefox-extension.zip
echo.
echo ------------------------------------------------
echo   INSTALLATION INSTRUCTIONS:
echo ------------------------------------------------
echo.
echo   CHROME:
echo     1. Extract chrome-extension.zip
echo     2. Go to chrome://extensions
echo     3. Enable "Developer mode" (top right)
echo     4. Click "Load unpacked"
echo     5. Select the extracted folder
echo.
echo   FIREFOX (Temporary - for testing):
echo     1. Extract firefox-extension.zip
echo     2. Go to about:debugging#/runtime/this-firefox
echo     3. Click "Load Temporary Add-on"
echo     4. Select manifest.json from extracted folder
echo.
echo   FIREFOX (Permanent - requires signing):
echo     1. Create account at https://addons.mozilla.org
echo     2. Go to Developer Hub ^> Submit New Add-on
echo     3. Upload firefox-extension.zip
echo     4. Choose "Self-distribution" for signed .xpi
echo     5. Share the signed .xpi file
echo.
echo ================================================
echo   IMPORTANT: Native Host Setup Required!
echo ================================================
echo   Users must also:
echo     1. Install Python 3.9+ and FFmpeg
echo     2. Run: pip install psutil
echo     3. Run install_host.bat (Windows)
echo        or install_host.sh (Mac/Linux)
echo ================================================
echo.
pause
