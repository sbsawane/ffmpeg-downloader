@echo off
REM Package extension for distribution
REM Creates ZIP files for Chrome and Firefox
setlocal enabledelayedexpansion

echo ================================================
echo   FFmpeg Stream Downloader - Packager
echo ================================================
echo.

REM Read version from VERSION file
set /p VERSION=<VERSION
echo   Version: %VERSION%
echo.

REM Create dist folder
if not exist "dist" mkdir "dist"

echo [1/4] Updating manifest versions...
REM Ensure manifests have correct version
powershell -Command "$content = Get-Content 'extension\manifest.json' -Raw; $content = $content -replace '\"version\": \"[^\"]+\"', '\"version\": \"%VERSION%\"'; Set-Content 'extension\manifest.json' $content -NoNewline"
powershell -Command "$content = Get-Content 'extension\manifest-firefox.json' -Raw; $content = $content -replace '\"version\": \"[^\"]+\"', '\"version\": \"%VERSION%\"'; Set-Content 'extension\manifest-firefox.json' $content -NoNewline"
echo       Manifests updated to v%VERSION%

echo.
echo [2/4] Packaging Chrome extension...
if exist "dist\chrome-extension-v%VERSION%.zip" del "dist\chrome-extension-v%VERSION%.zip"
powershell -Command "Compress-Archive -Path 'extension\manifest.json','extension\background.js','extension\popup.html','extension\popup.js' -DestinationPath 'dist\chrome-extension-v%VERSION%.zip' -Force"
echo       Created: dist\chrome-extension-v%VERSION%.zip

echo.
echo [3/4] Building Firefox extension...
if exist "build\firefox" rmdir /s /q "build\firefox"
mkdir "build\firefox"
copy "extension\background.js" "build\firefox\" >nul
copy "extension\popup.html" "build\firefox\" >nul
copy "extension\popup.js" "build\firefox\" >nul
copy "extension\manifest-firefox.json" "build\firefox\manifest.json" >nul

echo [4/4] Packaging Firefox extension...
if exist "dist\firefox-extension-v%VERSION%.zip" del "dist\firefox-extension-v%VERSION%.zip"
powershell -Command "Compress-Archive -Path 'build\firefox\*' -DestinationPath 'dist\firefox-extension-v%VERSION%.zip' -Force"
echo       Created: dist\firefox-extension-v%VERSION%.zip

echo.
echo ================================================
echo   Packages created in 'dist' folder:
echo ================================================
echo.
echo   Version: %VERSION%
echo   Chrome:  dist\chrome-extension-v%VERSION%.zip
echo   Firefox: dist\firefox-extension-v%VERSION%.zip
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
