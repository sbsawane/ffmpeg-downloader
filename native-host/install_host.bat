@REM @echo off
@REM :: Change this key to match the location of your JSON manifest
@REM REG ADD "HKCU\Software\Google\Chrome\NativeMessagingHosts\com.my_downloader" /ve /t REG_SZ /d "%~dp0com.my_downloader.json" /f
@REM echo Native Host Registered Successfully!
@REM pause

@echo off
:: %~dp0 automatically gets the current folder path
REG ADD "HKCU\Software\Google\Chrome\NativeMessagingHosts\com.my_downloader" /ve /t REG_SZ /d "%~dp0com.my_downloader.json" /f
echo Native Host Registered!
pause