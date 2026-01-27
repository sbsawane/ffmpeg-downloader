@echo off
:: Use python from PATH with unbuffered output for native messaging
python -u "%~dp0host.py" 2>&1