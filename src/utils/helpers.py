"""Helper utilities for Melbourne AI pipeline"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import subprocess


def get_timestamp(format_str: str = "%Y%m%d_%H%M%S") -> str:
    """Get current timestamp as string

    Args:
        format_str: Datetime format string

    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime(format_str)


def create_project_directory(base_dir: str = "outputs") -> str:
    """Create timestamped project directory structure

    Args:
        base_dir: Base output directory

    Returns:
        Path to created project directory
    """
    timestamp = get_timestamp()
    project_dir = os.path.join(base_dir, f"project_{timestamp}")

    # Create subdirectories
    subdirs = ["scripts", "images", "animations", "audio", "videos", "metadata"]
    for subdir in subdirs:
        os.makedirs(os.path.join(project_dir, subdir), exist_ok=True)

    return project_dir


def save_metadata(metadata: Dict[str, Any], output_path: str) -> None:
    """Save metadata to JSON file

    Args:
        metadata: Dictionary of metadata
        output_path: Path to save metadata file
    """
    with open(output_path, "w") as f:
        json.dump(metadata, f, indent=2)


def load_metadata(metadata_path: str) -> Dict[str, Any]:
    """Load metadata from JSON file

    Args:
        metadata_path: Path to metadata file

    Returns:
        Loaded metadata dictionary
    """
    with open(metadata_path, "r") as f:
        return json.load(f)


def check_ffmpeg() -> bool:
    """Check if FFmpeg is installed

    Returns:
        True if FFmpeg is available, False otherwise
    """
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_cuda_available() -> bool:
    """Check if CUDA/GPU is available

    Returns:
        True if CUDA is available, False otherwise
    """
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False


def get_device_type() -> str:
    """Get the device type for model inference

    Returns:
        Device type string ("cuda" or "cpu")
    """
    if check_cuda_available():
        return "cuda"
    return "cpu"


def format_duration(seconds: float) -> str:
    """Format duration in seconds to HH:MM:SS format

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def get_file_size(file_path: str) -> str:
    """Get human-readable file size

    Args:
        file_path: Path to file

    Returns:
        Human-readable file size string
    """
    size_bytes = os.path.getsize(file_path)
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def list_files_in_directory(directory: str, extension: str = None) -> List[str]:
    """List all files in a directory, optionally filtered by extension

    Args:
        directory: Directory path
        extension: Optional file extension filter (e.g., ".mp4")

    Returns:
        List of file paths
    """
    files = []
    if not os.path.exists(directory):
        return files

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if extension is None or filename.endswith(extension):
                files.append(filepath)
    return files


def ensure_directory_exists(directory: str) -> str:
    """Ensure a directory exists, create if needed

    Args:
        directory: Directory path

    Returns:
        Directory path
    """
    os.makedirs(directory, exist_ok=True)
    return directory


def clean_filename(filename: str) -> str:
    """Clean filename by removing invalid characters

    Args:
        filename: Original filename

    Returns:
        Cleaned filename
    """
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename
