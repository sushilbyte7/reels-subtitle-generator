# How to Use

## 🚀 Quick Start (Web UI - Recommended)

**Option 1: Double-click file**
- Just double-click `start_ui.bat`
- Browser will automatically open at http://localhost:7860
- Upload video, select model, generate subtitles!

**Option 2: Run manually**
```bash
python app.py
```
Then open http://localhost:7860 in your browser

---

## 💻 Command Line Usage (Advanced)

If you prefer terminal:
```bash
python main.py -i "path/to/video.mp4"
```

**With options:**
```bash
python main.py -i "video.mp4" -o "C:\Users\chandan\Downloads" -m large
```

---

## 📋 What You Need

1. ✅ Python installed
2. ✅ FFmpeg installed (already done via `winget install ffmpeg`)
3. ✅ Whisper installed (already done via `pip install -U openai-whisper`)
4. ✅ Gradio installed (already done via `pip install gradio`)

---

## 🎯 Choose Your Method

| Method | When to Use |
|--------|-------------|
| **Web UI** (`app.py`) | Easy, visual, drag & drop |
| **CLI** (`main.py`) | Automation, scripts, batch processing |

Both generate the same quality subtitles!
