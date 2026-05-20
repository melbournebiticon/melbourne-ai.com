#!/usr/bin/env python3
"""Flask Web Application for Melbourne AI Video Creator

Run with: python web/app.py
Access at: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import create_video_from_prompt
from src.utils.logger import setup_logger
from src.utils.helpers import list_files_in_directory

app = Flask(__name__, template_folder="templates", static_folder="static")
logger = setup_logger("flask-app")

# Configuration
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max
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


@app.route("/")
def index():
    """Main page"""
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def api_generate():
    """API endpoint to generate video"""
    try:
        data = request.json
        prompt = data.get("prompt", "").strip()
        duration = int(data.get("duration", 60))
        style = data.get("style", "general")
        voice = data.get("voice", "female")

        # Validate input
        if not prompt:
            return jsonify({"status": "error", "message": "Prompt is required"}), 400

        if duration < 30 or duration > 600:
            return jsonify({"status": "error", "message": "Duration must be between 30 and 600 seconds"}), 400

        logger.info(f"Video generation request: {prompt}")

        # Generate video
        video_path = create_video_from_prompt(
            prompt=prompt,
            duration=duration,
            style=style,
            voice=voice,
            output_dir="outputs",
        )

        # Save to history
        history = load_project_history()
        history.append(
            {
                "prompt": prompt,
                "duration": duration,
                "style": style,
                "voice": voice,
                "video_path": video_path,
                "timestamp": datetime.now().isoformat(),
            }
        )
        save_project_history(history)

        logger.info(f"Video generated successfully: {video_path}")

        return jsonify(
            {
                "status": "success",
                "message": "Video generated successfully!",
                "video_path": video_path,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"Error generating video: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/history", methods=["GET"])
def api_history():
    """Get project history"""
    try:
        history = load_project_history()
        # Return last 20 projects
        return jsonify({"status": "success", "data": history[-20:]})
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/videos", methods=["GET"])
def api_videos():
    """List available videos"""
    try:
        outputs_dir = "outputs"
        if not os.path.exists(outputs_dir):
            return jsonify({"status": "success", "data": []})

        videos = []
        for project_dir in os.listdir(outputs_dir):
            project_path = os.path.join(outputs_dir, project_dir)
            videos_path = os.path.join(project_path, "videos")
            if os.path.isdir(videos_path):
                for video_file in os.listdir(videos_path):
                    if video_file.endswith(".mp4"):
                        videos.append(
                            {
                                "name": video_file,
                                "path": os.path.join(videos_path, video_file),
                                "project": project_dir,
                            }
                        )

        return jsonify({"status": "success", "data": videos})
    except Exception as e:
        logger.error(f"Error listing videos: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/config", methods=["GET"])
def api_config():
    """Get configuration options"""
    return jsonify(
        {
            "styles": ["educational", "entertaining", "informative", "general"],
            "voices": ["female", "male"],
            "duration_range": {"min": 30, "max": 600, "default": 60},
        }
    )


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {str(error)}")
    return render_template("500.html"), 500


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎬 Melbourne AI Video Creator - Flask Web App")
    print("="*60)
    print("\n🌐 Launching web server...")
    print("📱 Access at: http://localhost:5000")
    print("\n⚠️  Make sure you have installed all dependencies:")
    print("   pip install -r requirements.txt")
    print("   pip install flask")
    print("\n🛑 Press Ctrl+C to stop the server\n")

    app.run(debug=True, host="0.0.0.0", port=5000)
