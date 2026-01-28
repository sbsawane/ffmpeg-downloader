@echo off
REM Generate PNG icons from SVG using PowerShell
REM Requires: Inkscape OR use online converter
REM This script provides multiple methods

echo ================================================
echo   Icon Generator for FFmpeg Stream Downloader
echo ================================================
echo.

set ICONS_DIR=extension\icons
set SVG_FILE=%ICONS_DIR%\icon.svg

REM Check if SVG exists
if not exist "%SVG_FILE%" (
    echo ERROR: %SVG_FILE% not found!
    exit /b 1
)

REM Method 1: Try Inkscape (if installed)
where inkscape >nul 2>&1
if %errorlevel% equ 0 (
    echo Using Inkscape to generate PNGs...
    inkscape "%SVG_FILE%" -w 16 -h 16 -o "%ICONS_DIR%\icon-16.png"
    inkscape "%SVG_FILE%" -w 32 -h 32 -o "%ICONS_DIR%\icon-32.png"
    inkscape "%SVG_FILE%" -w 48 -h 48 -o "%ICONS_DIR%\icon-48.png"
    inkscape "%SVG_FILE%" -w 128 -h 128 -o "%ICONS_DIR%\icon-128.png"
    echo Done!
    goto :verify
)

REM Method 2: Try ImageMagick (if installed)
where magick >nul 2>&1
if %errorlevel% equ 0 (
    echo Using ImageMagick to generate PNGs...
    magick "%SVG_FILE%" -resize 16x16 "%ICONS_DIR%\icon-16.png"
    magick "%SVG_FILE%" -resize 32x32 "%ICONS_DIR%\icon-32.png"
    magick "%SVG_FILE%" -resize 48x48 "%ICONS_DIR%\icon-48.png"
    magick "%SVG_FILE%" -resize 128x128 "%ICONS_DIR%\icon-128.png"
    echo Done!
    goto :verify
)

REM Method 3: Manual instructions
echo.
echo No image converter found (Inkscape or ImageMagick).
echo.
echo Please generate PNG icons manually:
echo.
echo Option A - Use online converter:
echo   1. Go to https://svgtopng.com/ or https://cloudconvert.com/svg-to-png
echo   2. Upload: %CD%\%SVG_FILE%
echo   3. Download as PNG in these sizes: 16, 32, 48, 128
echo   4. Save to: %CD%\%ICONS_DIR%\
echo      - icon-16.png
echo      - icon-32.png
echo      - icon-48.png
echo      - icon-128.png
echo.
echo Option B - Install Inkscape:
echo   winget install Inkscape.Inkscape
echo   Then run this script again.
echo.
echo Option C - Install ImageMagick:
echo   winget install ImageMagick.ImageMagick
echo   Then run this script again.
echo.
goto :end

:verify
echo.
echo Verifying generated icons...
if exist "%ICONS_DIR%\icon-16.png" (echo   [OK] icon-16.png) else (echo   [MISSING] icon-16.png)
if exist "%ICONS_DIR%\icon-32.png" (echo   [OK] icon-32.png) else (echo   [MISSING] icon-32.png)
if exist "%ICONS_DIR%\icon-48.png" (echo   [OK] icon-48.png) else (echo   [MISSING] icon-48.png)
if exist "%ICONS_DIR%\icon-128.png" (echo   [OK] icon-128.png) else (echo   [MISSING] icon-128.png)

:end
echo.
pause
