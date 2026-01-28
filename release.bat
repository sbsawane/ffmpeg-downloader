@echo off
REM ================================================
REM   Release Script - One command to release
REM   Usage: release.bat [major|minor|patch]
REM ================================================
setlocal enabledelayedexpansion

set BUMP_TYPE=%1
if "%BUMP_TYPE%"=="" set BUMP_TYPE=patch

echo.
echo ================================================
echo   FFmpeg Stream Downloader - Release
echo ================================================
echo   Bump type: %BUMP_TYPE%
echo ================================================
echo.

REM Step 1: Bump version
echo [Step 1/4] Bumping version...
call version.bat %BUMP_TYPE%

REM Read new version
set /p VERSION=<VERSION
echo.

REM Step 2: Package
echo [Step 2/4] Creating packages...
call package.bat
echo.

REM Step 3: Git commit
echo [Step 3/4] Committing changes...
git add -A
git commit -m "Release v%VERSION%"
echo.

REM Step 4: Tag and push
echo [Step 4/4] Creating tag and pushing...
git tag v%VERSION%
git push origin main
git push origin v%VERSION%

echo.
echo ================================================
echo   ✓ Release v%VERSION% complete!
echo ================================================
echo.
echo   Packages:
echo     - dist\chrome-extension-v%VERSION%.zip
echo     - dist\firefox-extension-v%VERSION%.zip
echo.
echo   Git:
echo     - Committed and pushed to main
echo     - Tagged as v%VERSION%
echo.
pause
