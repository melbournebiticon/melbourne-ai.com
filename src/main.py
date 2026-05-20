#!/usr/bin/env python3
"""Main entry point for Melbourne AI Video Creator"""

import argparse
import sys
from pathlib import Path

from src.utils.logger import setup_logger
from src.utils.config import get_config
from src.utils.helpers import create_project_directory, save_metadata
from src.scripts import (
    ScriptGenerator,
    ImageGenerator,
    Animator,
    TTSGenerator,
    VideoEditor,
)

# Setup logger
logger = setup_logger("melbourne-ai", level=20)  # INFO level


def create_video_from_prompt(
    prompt: str,
    duration: int = 60,
    style: str = "general",
    voice: str = "female",
    output_dir: str = "outputs",
    skip_animation: bool = False,
    debug: bool = False,
) -> str:
    """Complete pipeline: Create video from prompt

    Args:
        prompt: User-provided topic or description
        duration: Target video duration in seconds
        style: Content style (educational, entertaining, informative, etc.)
        voice: Voice for TTS (female, male)
        output_dir: Base output directory
        skip_animation: Skip animation stage for faster processing
        debug: Enable debug logging

    Returns:
        Path to generated video file
    """
    # Create project directory
    project_dir = create_project_directory(output_dir)
    logger.info(f"Project directory created: {project_dir}")

    # Load configuration
    config = get_config()
    config.tts_config.voice = voice

    try:
        # Step 1: Generate Script
        logger.info("\n=== Step 1: Script Generation ===")
        script_gen = ScriptGenerator()
        script = script_gen.generate(prompt)
        script_path = Path(project_dir) / "scripts" / "script.json"
        script_gen.save_script(script, str(script_path))
        logger.info(f"✓ Script generated: {script_path}")

        # Step 2: Generate Images
        logger.info("\n=== Step 2: AI Image Generation ===")
        image_gen = ImageGenerator()
        scene_prompts = script_gen.extract_scene_prompts(script)
        images_dir = Path(project_dir) / "images"
        image_metadata = image_gen.generate_images(scene_prompts, str(images_dir))
        logger.info(f"✓ Generated {len(image_metadata)} images")

        # Step 3: Animate Images
        if not skip_animation:
            logger.info("\n=== Step 3: Image Animation ===")
            animator = Animator()
            animations_dir = Path(project_dir) / "animations"
            image_paths = [img["output_path"] for img in image_metadata]
            animated_clips = animator.animate_images(image_paths, str(animations_dir))
            logger.info(f"✓ Created {len(animated_clips)} animated clips")
        else:
            logger.info("\n=== Step 3: Image Animation (SKIPPED) ===")
            animated_clips = image_metadata

        # Step 4: Generate Voiceover
        logger.info("\n=== Step 4: Text-to-Speech Voiceover ===")
        tts_gen = TTSGenerator()
        audio_dir = Path(project_dir) / "audio"
        narration_text = script.get("narration", "")
        audio_path = str(audio_dir / "narration.wav")
        audio_metadata = tts_gen.generate_voiceover(narration_text, audio_path)
        logger.info(f"✓ Voiceover generated: {audio_path}")

        # Step 5: Assemble Final Video
        logger.info("\n=== Step 5: Video Assembly & Editing ===")
        video_editor = VideoEditor()
        videos_dir = Path(project_dir) / "videos"
        final_video_path = str(videos_dir / "final_video.mp4")
        clip_paths = [clip["output_clip"] if "output_clip" in clip else clip["output_path"] for clip in animated_clips]
        video_metadata = video_editor.create_video(
            video_clips=clip_paths,
            audio_file=audio_path,
            output_path=final_video_path,
        )
        logger.info(f"✓ Final video created: {final_video_path}")

        # Save project metadata
        metadata_path = Path(project_dir) / "metadata" / "project_metadata.json"
        project_metadata = {
            "prompt": prompt,
            "duration": duration,
            "style": style,
            "voice": voice,
            "script_path": str(script_path),
            "images_count": len(image_metadata),
            "audio_path": audio_path,
            "final_video_path": final_video_path,
        }
        save_metadata(project_metadata, str(metadata_path))
        logger.info(f"✓ Metadata saved: {metadata_path}")

        logger.info("\n" + "="*50)
        logger.info("✓ VIDEO GENERATION COMPLETED SUCCESSFULLY!")
        logger.info(f"Output directory: {project_dir}")
        logger.info(f"Final video: {final_video_path}")
        logger.info("="*50 + "\n")

        return final_video_path

    except Exception as e:
        logger.error(f"\n✗ Error during video generation: {str(e)}", exc_info=debug)
        sys.exit(1)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Melbourne AI - Automated Video Content Creator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py --prompt "Educational video about photosynthesis"
  python src/main.py --prompt "Product review" --duration 120 --style entertaining
  python src/main.py --prompt "Tutorial" --voice male --skip-animation
        """,
    )

    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Main topic or description for the video",
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Target video duration in seconds (default: 60)",
    )

    parser.add_argument(
        "--style",
        type=str,
        default="general",
        choices=["educational", "entertaining", "informative", "general"],
        help="Content style (default: general)",
    )

    parser.add_argument(
        "--voice",
        type=str,
        default="female",
        choices=["male", "female"],
        help="Voiceover voice type (default: female)",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="outputs",
        help="Base output directory (default: outputs)",
    )

    parser.add_argument(
        "--skip-animation",
        action="store_true",
        help="Skip animation stage for faster processing",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging and full error tracebacks",
    )

    args = parser.parse_args()

    # Run the pipeline
    video_path = create_video_from_prompt(
        prompt=args.prompt,
        duration=args.duration,
        style=args.style,
        voice=args.voice,
        output_dir=args.output,
        skip_animation=args.skip_animation,
        debug=args.debug,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
