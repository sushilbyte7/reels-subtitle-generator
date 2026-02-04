import whisper
import datetime
import gradio as gr
import os
from pathlib import Path
import tempfile
import time

def format_timestamp(seconds: float):
    td = datetime.timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int(td.microseconds / 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def format_time_remaining(seconds):
    """Format remaining time in human readable format"""
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours}h {minutes}m"

def generate_subtitles(video_file, model_type, progress=gr.Progress()):
    if video_file is None:
        return None, "❌ Please upload a video file first!"
    
    try:
        start_time = time.time()
        
        # Progress update
        progress(0.1, desc="Loading AI model...")
        
        # Load Whisper model
        model = whisper.load_model(model_type)
        
        # Get video path
        video_path = Path(video_file)
        output_filename = video_path.parent / f"{video_path.stem}_subs.srt"
        
        # Progress update
        model_load_time = time.time() - start_time
        progress(0.3, desc="Transcribing video with AI...")
        
        # Transcribe with word timestamps
        transcribe_start = time.time()
        result = model.transcribe(str(video_path), word_timestamps=True)
        transcribe_time = time.time() - transcribe_start
        
        # Calculate estimated total time and remaining
        elapsed = time.time() - start_time
        estimated_total = elapsed / 0.7  # We're at 70% now
        remaining = estimated_total - elapsed
        
        # Progress update
        progress(0.7, desc=f"Generating subtitle file... (~{format_time_remaining(remaining)} left)")
        
        # Write SRT file
        with open(output_filename, "w", encoding="utf-8") as f:
            counter = 1
            for segment in result["segments"]:
                for word_data in segment["words"]:
                    word = word_data["word"].strip().replace(",", "")
                    
                    if not word:
                        continue

                    start = word_data["start"]
                    end = word_data["end"]

                    f.write(f"{counter}\n")
                    f.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
                    f.write(f"{word}\n\n")
                    counter += 1
        
        # Progress update
        progress(1.0, desc="Complete!")
        
        total_time = time.time() - start_time
        time_str = format_time_remaining(total_time)
        
        success_msg = f"✅ Success! Generated {counter-1} subtitle entries.\n\n⏱️ Processing time: {time_str}\n\n📥 Download your SRT file using the button above!"
        
        return str(output_filename), success_msg
        
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

# Custom CSS for modern SaaS design
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    /* Modern SaaS Palette (Indigo/Slate) */
    --primary: #6366f1;
    --primary-hover: #4f46e5;
    --secondary: #64748b;
    --background: #0f172a;
    --surface: rgba(30, 41, 59, 0.7);
    --surface-hover: rgba(30, 41, 59, 0.9);
    --border: rgba(255, 255, 255, 0.1);
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    
    /* Effects */
    --glass: blur(12px) saturate(180%);
    --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.15);
    
    /* Layout */
    --radius: 16px;
}

body, .gradio-container {
    background-color: var(--background) !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(56, 189, 248, 0.15) 0px, transparent 50%);
    font-family: 'Inter', system-ui, sans-serif !important;
    color: var(--text-main) !important;
}

/* Glassmorphism Panels */
/* Glassmorphism Panels */
.glass-card {
    background: var(--surface) !important;
    backdrop-filter: var(--glass);
    -webkit-backdrop-filter: var(--glass);
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-sm) !important;
    padding: 2rem !important;
    height: 100% !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card:hover {
    box-shadow: var(--shadow-md), var(--shadow-glow) !important;
    border-color: rgba(99, 102, 241, 0.3) !important;
    transform: translateY(-2px);
}

/* Typography */
h1, h2, h3, h4, .gr-markdown h1, .gr-markdown h2, .gr-markdown h3 {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-main) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

.gr-markdown p {
    color: var(--text-muted) !important;
    line-height: 1.6;
    font-size: 1.05rem;
}

/* Inputs & Forms */
.gr-input, .gr-textbox, .gr-dropdown {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-main) !important;
    transition: all 0.2s ease;
}

.gr-input:focus, .gr-textbox:focus, .gr-dropdown:focus-within {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    background: rgba(15, 23, 42, 0.8) !important;
}

/* Buttons */
.action-btn {

    background: linear-gradient(135deg, var(--primary), var(--primary-hover)) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
    transition: all 0.3s ease !important;
}

.action-btn:hover {

    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4) !important;
}

/* File Upload */
.gr-file {
    border: 2px dashed rgba(255, 255, 255, 0.1) !important;
    background: rgba(255, 255, 255, 0.02) !important;
    border-radius: var(--radius) !important;
}

.gr-file:hover {
    border-color: var(--primary) !important;
    background: rgba(99, 102, 241, 0.05) !important;
}

/* Status Output */
.gr-textbox textarea {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    color: #a5b4fc !important;
}

/* Footer & Accents */
a {
    color: var(--primary) !important;
    text-decoration: none;
    transition: color 0.2s;
}

a:hover {
    color: #818cf8 !important;
    text-decoration: underline;
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.gradio-container > * {
    animation: fadeIn 0.6s ease-out;
}
"""

# Create Gradio Interface with Modern Theme
with gr.Blocks(title="Subtitle Generator - AI-Powered") as app:
    
    gr.Markdown(
        """
        # 🎬 One-Word Subtitle Generator
        ### AI-powered subtitle generation for viral content
        
        Transform your videos with perfectly timed subtitles in minutes
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1, elem_classes="glass-card"):

            # Input section
            gr.Markdown("### 📤 Upload & Settings")
            
            video_input = gr.File(
                label="Video File",
                file_types=["video"],
                type="filepath"
            )
            
            model_dropdown = gr.Dropdown(
                choices=["tiny", "base", "small", "medium", "large", "turbo"],
                value="turbo",
                label="AI Model",
                info="Balance between speed and accuracy"
            )
            
            generate_btn = gr.Button("Generate Subtitles", variant="primary", size="lg", elem_classes="action-btn")

            
            gr.Markdown(
                """
                ### 💡 Model Guide
                **Turbo** — Fast processing (2-3 mins) • _Recommended_  
                **Large** — Highest accuracy (5-7 mins) • For technical content  
                **Medium** — Balanced (4-5 mins)  
                **Small** — Quick results (1-2 mins)
                
                > Average processing time: 2-5 minutes depending on model selection
                """
            )
        
        with gr.Column(scale=1, elem_classes="glass-card"):

            # Output section
            gr.Markdown("### 📥 Results")
            
            output_file = gr.File(label="Download Subtitle File")
            output_message = gr.Textbox(
                label="Status",
                lines=6,
                interactive=False,
                placeholder="Processing status will appear here..."
            )
            
            gr.Markdown(
                """
                ### 📱 Import to Editor
                
                **CapCut**  
                Text → Captions → Import SRT → Upload file → Apply animations
                
                **VN Video Editor**  
                Text → Subtitle → Import SRT → Select file → Customize style
                
                > 💡 **Tip**: Use "Pop" or "Bounce" animations for maximum engagement
                """
            )
    
    # Footer
    gr.Markdown(
        """
        ---
        
        Built with ❤️ by [Sushil Kumar](https://github.com/sushilbyte7) • 
        Powered by [OpenAI Whisper](https://github.com/openai/whisper)
        
        [GitHub Repository](https://github.com/sushilbyte7/reels-subtitle-generator) • ⭐ Star if you find it useful
        """
    )
    
    # Connect button to function
    generate_btn.click(
        fn=generate_subtitles,
        inputs=[video_input, model_dropdown],
        outputs=[output_file, output_message]
    )

# Launch the app
if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True,
        css=custom_css,
        theme=gr.themes.Soft()
    )
