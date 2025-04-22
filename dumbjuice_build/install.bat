@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0appfolder\build.ps1"
pause
