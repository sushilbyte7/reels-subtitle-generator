@echo off
echo Starting One-Word Subtitle Generator UI...
echo.

REM Update PATH to include FFmpeg
set PATH=%PATH%;C:\ffmpeg\bin

REM Start the app
python app.py

pause
