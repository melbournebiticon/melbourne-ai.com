"""Configuration management for Melbourne AI pipeline"""

import os
from typing import Dict, Any
from pydantic import BaseModel
import yaml


class ImageConfig(BaseModel):
    """Image generation configuration"""
    model: str = "runwayml/stable-diffusion-v1-5"
    resolution: tuple = (768, 768)
    num_inference_steps: int = 50
    guidance_scale: float = 7.5
    batch_size: int = 4
    num_images_per_scene: int = 1
    seed: int = 42


class AnimationConfig(BaseModel):
    """Animation configuration"""
    effect_type: str = "ken_burns"  # ken_burns, fade, zoom, slide, wipe
    duration: float = 5.0  # seconds per image
    transition_duration: float = 1.0
    fps: int = 24
    deforum_enabled: bool = False


class TTSConfig(BaseModel):
    """Text-to-Speech configuration"""
    engine: str = "coqui"  # coqui, vits, glow_tts
    language: str = "en"
    voice: str = "female"  # female, male
    speed: float = 1.0
    pitch: float = 1.0
    sample_rate: int = 22050


class VideoConfig(BaseModel):
    """Video assembly configuration"""
    output_format: str = "mp4"
    resolution: tuple = (1920, 1080)
    fps: int = 24
    bitrate: str = "5000k"
    audio_bitrate: str = "192k"
    include_subtitles: bool = True
    subtitle_style: str = "default"


class ScriptConfig(BaseModel):
    """Script generation configuration"""
    llm_model: str = "llama2"  # llama2, mistral, neural-chat
    max_tokens: int = 2000
    temperature: float = 0.7
    top_p: float = 0.9
    min_scenes: int = 3
    max_scenes: int = 10


class Config:
    """Main configuration class"""

    def __init__(self, config_file: str = None):
        self.image_config = ImageConfig()
        self.animation_config = AnimationConfig()
        self.tts_config = TTSConfig()
        self.video_config = VideoConfig()
        self.script_config = ScriptConfig()

        self.project_dir = os.path.join(os.getcwd(), "outputs")
        self.models_dir = os.path.join(os.getcwd(), "models")
        self.assets_dir = os.path.join(os.getcwd(), "assets")

        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)

    def load_from_file(self, config_file: str) -> None:
        """Load configuration from YAML file"""
        with open(config_file, "r") as f:
            config_data = yaml.safe_load(f)

        if "image" in config_data:
            self.image_config = ImageConfig(**config_data["image"])
        if "animation" in config_data:
            self.animation_config = AnimationConfig(**config_data["animation"])
        if "tts" in config_data:
            self.tts_config = TTSConfig(**config_data["tts"])
        if "video" in config_data:
            self.video_config = VideoConfig(**config_data["video"])
        if "script" in config_data:
            self.script_config = ScriptConfig(**config_data["script"])

    def save_to_file(self, config_file: str) -> None:
        """Save configuration to YAML file"""
        config_dict = {
            "image": self.image_config.dict(),
            "animation": self.animation_config.dict(),
            "tts": self.tts_config.dict(),
            "video": self.video_config.dict(),
            "script": self.script_config.dict(),
        }

        with open(config_file, "w") as f:
            yaml.dump(config_dict, f, default_flow_style=False)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "image": self.image_config.dict(),
            "animation": self.animation_config.dict(),
            "tts": self.tts_config.dict(),
            "video": self.video_config.dict(),
            "script": self.script_config.dict(),
        }


# Global config instance
_config = None


def get_config(config_file: str = None) -> Config:
    """Get or create global config instance"""
    global _config
    if _config is None:
        _config = Config(config_file)
    return _config
