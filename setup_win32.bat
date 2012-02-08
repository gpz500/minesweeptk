@echo off
rmdir /s /q dist 2>nul
rmdir /s /q build 2>nul
python setup_win32.py py2exe
if errorlevel 1 exit /b 1
copy *.gif dist
copy license.txt dist
