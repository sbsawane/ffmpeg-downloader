@echo off
REM ================================================
REM   Version Bump Script
REM   Usage: version.bat [major|minor|patch]
REM ================================================
setlocal enabledelayedexpansion

REM Read current version
set /p CURRENT_VERSION=<VERSION

REM Parse version parts
for /f "tokens=1,2,3 delims=." %%a in ("%CURRENT_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
    set PATCH=%%c
)

REM Default patch to 0 if not present
if "%PATCH%"=="" set PATCH=0

REM Determine bump type
set BUMP_TYPE=%1
if "%BUMP_TYPE%"=="" set BUMP_TYPE=patch

if "%BUMP_TYPE%"=="major" (
    set /a MAJOR+=1
    set MINOR=0
    set PATCH=0
) else if "%BUMP_TYPE%"=="minor" (
    set /a MINOR+=1
    set PATCH=0
) else if "%BUMP_TYPE%"=="patch" (
    set /a PATCH+=1
)

REM Build new version
if %PATCH%==0 (
    set NEW_VERSION=%MAJOR%.%MINOR%
) else (
    set NEW_VERSION=%MAJOR%.%MINOR%.%PATCH%
)

echo.
echo ================================================
echo   Version Update
echo ================================================
echo   Current: %CURRENT_VERSION%
echo   New:     %NEW_VERSION%
echo ================================================
echo.

REM Update VERSION file
echo %NEW_VERSION%> VERSION

REM Update Chrome manifest.json
powershell -Command "$content = Get-Content 'extension\manifest.json' -Raw; $content = $content -replace '\"version\": \"[^\"]+\"', '\"version\": \"%NEW_VERSION%\"'; Set-Content 'extension\manifest.json' $content -NoNewline"
echo Updated: extension\manifest.json

REM Update Firefox manifest-firefox.json
powershell -Command "$content = Get-Content 'extension\manifest-firefox.json' -Raw; $content = $content -replace '\"version\": \"[^\"]+\"', '\"version\": \"%NEW_VERSION%\"'; Set-Content 'extension\manifest-firefox.json' $content -NoNewline"
echo Updated: extension\manifest-firefox.json

echo.
echo ✓ Version bumped to %NEW_VERSION%
echo.
echo Next steps:
echo   1. Run: package.bat (to create new packages)
echo   2. Run: git add -A ^&^& git commit -m "Release v%NEW_VERSION%"
echo   3. Run: git tag v%NEW_VERSION% ^&^& git push --tags
echo.
