# Melbourne AI - Automated Video Content Creator

An open-source, self-hosted toolchain that transforms text prompts into unique, AI-generated videos with animations, voiceovers, and professional editing—perfect for content creators building niche channels on YouTube, Facebook, and beyond.

## 🎯 Project Goal

Turn a simple text prompt into a **finished, one-of-a-kind video** with:
- ✨ Unique AI-generated visuals (no stock footage)
- 🎬 Smooth animations (pan, zoom, morphing)
- 🎙️ Natural-sounding narration
- ✏️ Automatic editing, subtitles, transitions
- 🚀 Minimal manual intervention

## 🔄 Workflow Stages

```
User Prompt
   ↓
Script Generation (LLM) → Scene Descriptions
   ↓
AI Image Generation (Stable Diffusion) → Unique Images
   ↓
Image Animation (MoviePy/Deforum) → Animated Clips
   ↓
Voiceover Generation (TTS) → Narration Audio
   ↓
Video Assembly & Editing (MoviePy/FFmpeg) → Final Video
   ↓
Finishing Touches (Subtitles, Export) → Ready to Upload
```

### Detailed Stages:

1. **Prompt Ingestion:** User provides a topic or content idea
2. **Script Generation:** LLM expands prompt into scene-by-scene script
3. **Image Generation:** AI creates unique visuals for each scene (Stable Diffusion)
4. **Image Animation:** Convert static images into smooth animations
5. **Voiceover Generation:** Text-to-speech narration from the script
6. **Video Assembly & Editing:** Combine visuals, audio, music, transitions
7. **Finishing & Export:** Add subtitles, branding, quality enhancements

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Image Generation:** Stable Diffusion (via Diffusers or Automatic1111's WebUI)
- **Video Assembly:** MoviePy, FFmpeg
- **Text-to-Speech:** Coqui TTS or VITS
- **LLM for Scripts:** Ollama, LM Studio (local LLMs like Llama 3, Mixtral)
- **Optional UI:** Gradio (for web interface)
- **Music/Assets:** Free open-source or royalty-free resources

## 📋 Requirements

### Hardware
- **Minimum:** 8GB RAM, CPU-based processing (slow)
- **Recommended:** GPU (NVIDIA CUDA 12.0+ or AMD ROCm) for faster image/video generation

### Software
- Python 3.10 or higher
- FFmpeg installed on your system
- CUDA Toolkit (optional, for GPU acceleration)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/melbournebiticon/melbourne-ai.com.git
cd melbourne-ai.com
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Workflow
```bash
python src/main.py --prompt "Your video topic here"
```

## 📁 Project Structure

```
melbourne-ai.com/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── main.py                 # Main entry point
│   ├── scripts/
│   │   ├── __init__.py
│   │   ├── script_generator.py # LLM → Script
│   │   ├── image_generator.py  # Stable Diffusion → Images
│   │   ├── animator.py         # Images → Animation
│   │   ├── tts_generator.py    # Script → Voiceover
│   │   └── video_editor.py     # Assemble final video
│   └── utils/
│       ├── __init__.py
│       ├── config.py           # Configuration settings
│       ├── logger.py           # Logging utilities
│       └── helpers.py          # Helper functions
├── assets/
│   ├── templates/              # Prompt templates
│   ├── music/                  # Background music library
│   └── branding/               # Logos, intros, outros
├── outputs/
│   └── [generated videos & assets stored here]
└── docs/
    ├── SETUP.md                # Detailed setup guide
    ├── USAGE.md                # How to use the tool
    └── ARCHITECTURE.md         # Technical architecture
```

## 🎬 Usage Example

### Basic Usage
```python
from src.scripts import (
    script_generator,
    image_generator,
    animator,
    tts_generator,
    video_editor
)

# Define your prompt
prompt = "Create an educational video about the water cycle for children"

# Generate script
script = script_generator.generate(prompt)

# Generate images for each scene
images = image_generator.generate_from_scenes(script['scenes'])

# Animate images
animations = animator.animate(images)

# Generate voiceover
audio = tts_generator.generate(script['narration'])

# Assemble final video
video_editor.create_video(animations, audio, script)
```

## 🔧 Configuration

Edit `src/utils/config.py` to customize:
- Image resolution & style
- Animation speed & effects
- Voice (language, gender, speed)
- Video quality & format
- Output directories

## 📚 Documentation

- **[SETUP.md](docs/SETUP.md)** - Detailed installation for each OS
- **[USAGE.md](docs/USAGE.md)** - Complete usage guide with examples
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Technical deep-dive

## 💰 Cost

**Completely free!** All tools are:
- Open-source (no licensing fees)
- Self-hosted (no cloud costs)
- No API requirements (run locally)

## 🤝 Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your improvements
4. Submit a pull request

## 📝 License

[Choose a license: MIT, Apache 2.0, GPL 3.0, etc.]

## 🔗 Resources & Credits

- [Stable Diffusion](https://github.com/CompVis/stable-diffusion)
- [Automatic1111's SD WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [MoviePy](https://zulko.github.io/moviepy/)
- [Coqui TTS](https://github.com/coqui-ai/TTS)
- [Ollama](https://ollama.com/)
- [FFmpeg](https://ffmpeg.org/)

## 📞 Support & Feedback

- Open an issue for bugs or feature requests
- Discussions tab for general questions
- Check existing issues before submitting

---

**Happy creating! 🎥✨**
