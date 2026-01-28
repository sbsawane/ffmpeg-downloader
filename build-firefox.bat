@echo off
REM Build Firefox extension package
REM Creates a folder with manifest-firefox.json renamed to manifest.json

SET BUILD_DIR=build\firefox
SET SOURCE_DIR=extension

echo Building Firefox extension...

REM Clean and create build directory
if exist "%BUILD_DIR%" rmdir /s /q "%BUILD_DIR%"
mkdir "%BUILD_DIR%"
mkdir "%BUILD_DIR%\icons"

REM Copy all files except manifests
copy "%SOURCE_DIR%\background.js" "%BUILD_DIR%\"
copy "%SOURCE_DIR%\popup.html" "%BUILD_DIR%\"
copy "%SOURCE_DIR%\popup.js" "%BUILD_DIR%\"

REM Copy icons
copy "%SOURCE_DIR%\icons\*" "%BUILD_DIR%\icons\" >nul 2>nul

REM Copy Firefox manifest as manifest.json
copy "%SOURCE_DIR%\manifest-firefox.json" "%BUILD_DIR%\manifest.json"

echo.
echo ✓ Firefox extension built in: %BUILD_DIR%
echo.
echo To load in Firefox:
echo   1. Go to about:debugging#/runtime/this-firefox
echo   2. Click "Load Temporary Add-on..."
echo   3. Select: %CD%\%BUILD_DIR%\manifest.json
echo.
pause
