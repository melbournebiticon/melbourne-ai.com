"""Script generation module using LLM"""

import json
from typing import Dict, List, Any
from src.utils.logger import get_logger
from src.utils.config import get_config

logger = get_logger()


class ScriptGenerator:
    """Generate video scripts from prompts using LLM"""

    def __init__(self):
        self.config = get_config()
        self.llm_model = self.config.script_config.llm_model
        # TODO: Initialize Ollama or LM Studio connection
        logger.info(f"ScriptGenerator initialized with model: {self.llm_model}")

    def generate(self, prompt: str) -> Dict[str, Any]:
        """Generate video script from prompt

        Args:
            prompt: User-provided topic or description

        Returns:
            Dictionary containing script data with scenes and narration
        """
        logger.info(f"Generating script for prompt: {prompt}")

        # TODO: Call LLM (Ollama/LM Studio) to generate script
        # This should return:
        # {
        #     "title": "Video title",
        #     "narration": "Full narration text",
        #     "scenes": [
        #         {"scene_num": 1, "description": "...", "duration": 5, "narration_text": "..."},
        #         ...
        #     ]
        # }

        script = {
            "title": "Generated Video Title",
            "narration": "Full narration text will be generated here.",
            "scenes": [],
        }

        logger.info(f"Script generation completed with {len(script.get('scenes', []))} scenes")
        return script

    def extract_scene_prompts(self, script: Dict[str, Any]) -> List[str]:
        """Extract image generation prompts from script scenes

        Args:
            script: Generated script dictionary

        Returns:
            List of image prompts for each scene
        """
        scene_prompts = []
        for scene in script.get("scenes", []):
            prompt = f"{scene.get('description', '')} - {scene.get('narration_text', '')}"
            scene_prompts.append(prompt)

        logger.info(f"Extracted {len(scene_prompts)} scene prompts")
        return scene_prompts

    def save_script(self, script: Dict[str, Any], output_path: str) -> None:
        """Save generated script to JSON file

        Args:
            script: Script dictionary
            output_path: Path to save script file
        """
        with open(output_path, "w") as f:
            json.dump(script, f, indent=2)
        logger.info(f"Script saved to {output_path}")
