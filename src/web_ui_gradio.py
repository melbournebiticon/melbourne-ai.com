#!/usr/bin/env python3
"""Gradio Web UI for Melbourne AI Video Creator

Run with: python src/web_ui_gradio.py
Access at: http://localhost:7860
"""

import gradio as gr
import os
import json
from pathlib import Path
from src.main import create_video_from_prompt
from src.utils.logger import setup_logger

logger = setup_logger("web-ui")

# Store project history
PROJECT_HISTORY_FILE = "web_projects_history.json"


def load_project_history():
    """Load project history from file"""
    if os.path.exists(PROJECT_HISTORY_FILE):
        with open(PROJECT_HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_project_history(history):
    """Save project history to file"""
    with open(PROJECT_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def generate_video(
    prompt: str,
    duration: int,
    style: str,
    voice: str,
    progress=gr.Progress(),
):
    """Generate video from prompt

    Args:
        prompt: Video topic/description
        duration: Video duration in seconds
        style: Content style
        voice: Voice type for narration
        progress: Gradio progress tracker

    Returns:
        Tuple of (video_path, status_message)
    """
    try:
        if not prompt or len(prompt.strip()) == 0:
            return None, "❌ Error: Please enter a prompt"

        progress(0, desc="Starting video generation...")

        # Generate video
        video_path = create_video_from_prompt(
            prompt=prompt,
            duration=duration,
            style=style,
            voice=voice,
            output_dir="outputs",
            skip_animation=False,
            debug=False,
        )

        progress(1, desc="Video generation completed!")

        # Save to history
        history = load_project_history()
        history.append(
            {
                "prompt": prompt,
                "duration": duration,
                "style": style,
                "voice": voice,
                "video_path": video_path,
                "timestamp": str(Path(video_path).parent.parent.name),
            }
        )
        save_project_history(history)

        status_msg = f"✅ Video generated successfully!\n\nPath: {video_path}"
        logger.info(f"Video generated: {video_path}")

        return video_path, status_msg

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        logger.error(error_msg)
        return None, error_msg


def get_project_history():
    """Get formatted project history"""
    history = load_project_history()
    if not history:
        return "No projects generated yet"

    history_text = "**Recent Projects:**\n\n"
    for i, project in enumerate(reversed(history[-10:]), 1):  # Last 10
        history_text += f"{i}. **{project['prompt'][:50]}...** ({project['duration']}s)\n"
        history_text += f"   Style: {project['style']} | Voice: {project['voice']}\n"
        history_text += f"   Timestamp: {project['timestamp']}\n\n"

    return history_text


def create_gradio_interface():
    """Create and configure Gradio interface"""

    with gr.Blocks(
        title="Melbourne AI Video Creator",
        theme=gr.themes.Soft(primary_hue="blue"),
    ) as demo:
        gr.Markdown(
            """
        # 🎬 Melbourne AI Video Creator
        ### Automatically Generate Unique Videos from Text Prompts

        Transform your ideas into professional-quality videos with AI-generated visuals,
        animations, voiceovers, and automatic editing—all powered by open-source AI models.

        **Features:**
        - 🤖 AI-generated unique visuals (no stock footage)
        - ✨ Automatic animations and effects
        - 🎙️ Natural-sounding narration
        - 📹 Professional video editing
        - 🎯 Optimized for YouTube, Facebook, TikTok
        """
        )

        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("## 📝 Video Configuration")

                prompt_input = gr.Textbox(
                    label="📌 Video Prompt/Topic",
                    placeholder="e.g., 'Educational video about the water cycle for kids'",
                    lines=3,
                    info="Describe what your video should be about",
                )

                with gr.Row():
                    duration_slider = gr.Slider(
                        minimum=30,
                        maximum=600,
                        value=60,
                        step=10,
                        label="⏱️ Duration (seconds)",
                        info="Target video length",
                    )

                    style_dropdown = gr.Dropdown(
                        choices=["educational", "entertaining", "informative", "general"],
                        value="educational",
                        label="🎨 Content Style",
                        info="Type of content",
                    )

                with gr.Row():
                    voice_radio = gr.Radio(
                        choices=["female", "male"],
                        value="female",
                        label="🎙️ Narrator Voice",
                        info="Voiceover voice type",
                    )

                generate_btn = gr.Button(
                    "🚀 Generate Video",
                    variant="primary",
                    size="lg",
                )

            with gr.Column(scale=2):
                gr.Markdown("## 🎥 Video Output")

                video_output = gr.Video(
                    label="Generated Video",
                    format="mp4",
                )

                status_output = gr.Markdown(
                    "Status: Waiting for input...",
                    label="Status",
                )

        gr.Markdown("---")

        with gr.Row():
            with gr.Column():
                gr.Markdown("## 📊 Project History")
                history_btn = gr.Button("📜 Refresh History", size="sm")
                history_output = gr.Markdown(
                    label="Recent Projects",
                    value=get_project_history(),
                )

        # Event handlers
        generate_btn.click(
            fn=generate_video,
            inputs=[prompt_input, duration_slider, style_dropdown, voice_radio],
            outputs=[video_output, status_output],
        )

        history_btn.click(
            fn=lambda: get_project_history(),
            outputs=history_output,
        )

        # Auto-update history on page load
        demo.load(fn=lambda: get_project_history(), outputs=history_output)

    return demo


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎬 Melbourne AI Video Creator - Gradio Web UI")
    print("="*60)
    print("\n🌐 Launching web interface...")
    print("📱 Access at: http://localhost:7860")
    print("\n⚠️  Make sure you have installed all dependencies:")
    print("   pip install -r requirements.txt")
    print("\n🛑 Press Ctrl+C to stop the server\n")

    demo = create_gradio_interface()
    demo.launch(share=False, server_name="0.0.0.0", server_port=7860)
