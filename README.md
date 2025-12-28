# Netflix Food Cinematic Edit

A Python-based project that transforms food photography and video content with Netflix-style cinematic effects and editing capabilities. This tool leverages modern video processing and image enhancement techniques to create professional-grade, visually stunning culinary content.

## 🎬 Features

- **Cinematic Color Grading**: Apply Netflix-inspired color grades to food photography and videos
- **Dynamic Lighting Effects**: Enhance lighting and shadows for dramatic, professional-looking results
- **Audio Enhancement**: Optimize audio quality with Netflix-style sound mixing
- **Transition Effects**: Smooth, professional transitions between scenes
- **Batch Processing**: Process multiple files efficiently in bulk operations
- **Real-time Preview**: View effects in real-time before applying to final output
- **Customizable Presets**: Use or create custom effect presets
- **Multi-format Support**: Compatible with common video and image formats (MP4, MOV, PNG, JPG, etc.)
- **High-Performance Processing**: Optimized for fast rendering and minimal resource consumption

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 💻 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- FFmpeg installed and added to system PATH
- 4GB RAM minimum (8GB recommended)
- GPU support (optional but recommended for better performance)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Akane1221/netflix-food-cinematic-edit.git
cd netflix-food-cinematic-edit
```

### Step 2: Create a Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python -m netflix_food_cinematic_edit --version
```

## 🚀 Quick Start

### Basic Usage

```bash
# Apply default Netflix cinematic effect to a video
python -m netflix_food_cinematic_edit process input_video.mp4 -o output_video.mp4

# Apply to an image
python -m netflix_food_cinematic_edit process food_photo.jpg -o edited_photo.jpg

# Use a specific preset
python -m netflix_food_cinematic_edit process input.mp4 -o output.mp4 --preset dark_dramatic
```

### Using the Python API

```python
from netflix_food_cinematic_edit import CinematicEditor

# Initialize editor
editor = CinematicEditor()

# Process a video
editor.process_video('input_video.mp4', 'output_video.mp4', preset='netflix_dark')

# Or process an image
editor.process_image('food_photo.jpg', 'edited_photo.jpg', preset='warm_cinematic')
```

## 📖 Usage Guide

### Command Line Interface

#### Basic Command Structure

```bash
python -m netflix_food_cinematic_edit <command> <input_file> [options]
```

#### Available Commands

- `process` - Process a single file
- `batch` - Process multiple files
- `preview` - Preview effects without saving
- `list-presets` - Display all available presets
- `create-preset` - Create a custom preset

### Common Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output file path | `output_[timestamp].mp4` |
| `--preset` | `-p` | Effect preset to use | `netflix_cinematic` |
| `--quality` | `-q` | Output quality (low/med/high) | `high` |
| `--fps` | `None` | Output frame rate | Original |
| `--resolution` | `-r` | Output resolution (WIDTHxHEIGHT) | Original |
| `--brightness` | `-b` | Brightness adjustment (-100 to 100) | 0 |
| `--contrast` | `-c` | Contrast adjustment (-100 to 100) | 0 |
| `--saturation` | `-s` | Saturation adjustment (-100 to 100) | 0 |

### Examples

```bash
# High-quality cinematic processing
python -m netflix_food_cinematic_edit process cooking_video.mp4 \
  -o cinematic_output.mp4 \
  --preset netflix_dark \
  --quality high

# Batch process all MP4 files in a directory
python -m netflix_food_cinematic_edit batch ./videos/ \
  -o ./edited_videos/ \
  --preset warm_cinematic \
  --quality medium

# Preview effect before processing
python -m netflix_food_cinematic_edit preview food_photo.jpg --preset dark_dramatic

# Adjust specific parameters
python -m netflix_food_cinematic_edit process input.mp4 \
  -o output.mp4 \
  --brightness 10 \
  --contrast 15 \
  --saturation 5
```

### Available Presets

- **netflix_cinematic** - Classic Netflix dark, moody cinematic look
- **netflix_dark** - Enhanced dark tones with warm undertones
- **warm_cinematic** - Warm, inviting cinematic style
- **dark_dramatic** - High contrast, dramatic lighting
- **vibrant_food** - Enhanced colors optimized for food content
- **cool_blue** - Cool tones with blue undertones
- **vintage_film** - Classic film look with slight grain
- **minimalist** - Clean, modern, minimal color grading

## 📁 Project Structure

```
netflix-food-cinematic-edit/
├── README.md                          # This file
├── LICENSE                            # Project license
├── requirements.txt                   # Python dependencies
├── setup.py                           # Package setup configuration
│
├── netflix_food_cinematic_edit/       # Main package directory
│   ├── __init__.py                    # Package initialization
│   ├── __main__.py                    # CLI entry point
│   │
│   ├── core/                          # Core processing modules
│   │   ├── __init__.py
│   │   ├── editor.py                  # Main CinematicEditor class
│   │   ├── video_processor.py         # Video processing logic
│   │   ├── image_processor.py         # Image processing logic
│   │   ├── color_grading.py           # Color grading algorithms
│   │   └── effects.py                 # Effect implementations
│   │
│   ├── presets/                       # Effect presets
│   │   ├── __init__.py
│   │   ├── netflix_presets.py         # Netflix-style presets
│   │   ├── food_presets.py            # Food photography presets
│   │   └── custom_presets.py          # User custom presets
│   │
│   ├── utils/                         # Utility functions
│   │   ├── __init__.py
│   │   ├── ffmpeg_wrapper.py          # FFmpeg interface
│   │   ├── file_handler.py            # File operations
│   │   ├── validators.py              # Input validation
│   │   └── logger.py                  # Logging configuration
│   │
│   ├── config/                        # Configuration files
│   │   ├── __init__.py
│   │   ├── settings.py                # Default settings
│   │   └── constants.py               # Project constants
│   │
│   └── cli/                           # Command-line interface
│       ├── __init__.py
│       ├── commands.py                # CLI command definitions
│       ├── parser.py                  # Argument parser
│       └── output_formatter.py        # Output formatting
│
├── tests/                             # Test suite
│   ├── __init__.py
│   ├── test_editor.py                 # Editor tests
│   ├── test_video_processor.py        # Video processor tests
│   ├── test_image_processor.py        # Image processor tests
│   ├── test_presets.py                # Preset tests
│   └── fixtures/                      # Test fixtures and sample files
│
├── examples/                          # Usage examples
│   ├── basic_usage.py                 # Basic usage example
│   ├── batch_processing.py            # Batch processing example
│   ├── custom_preset.py               # Custom preset creation
│   └── advanced_effects.py            # Advanced effects example
│
├── docs/                              # Documentation
│   ├── INSTALLATION.md                # Detailed installation guide
│   ├── API.md                         # API reference
│   ├── PRESETS.md                     # Preset documentation
│   ├── TROUBLESHOOTING.md             # Troubleshooting guide
│   └── CONTRIBUTING.md                # Contribution guidelines
│
└── scripts/                           # Utility scripts
    ├── setup_environment.sh           # Environment setup script
    ├── install_ffmpeg.sh              # FFmpeg installation script
    └── generate_samples.py            # Sample generation script
```

## ⚙️ Configuration

### Configuration File

Create a `config.json` file in the project root for custom settings:

```json
{
  "default_preset": "netflix_cinematic",
  "output_quality": "high",
  "ffmpeg_threads": 4,
  "gpu_enabled": true,
  "temp_directory": "./temp",
  "logging_level": "INFO",
  "max_concurrent_jobs": 3
}
```

### Environment Variables

```bash
# Set default preset
export NETFLIX_PRESET=netflix_dark

# Enable GPU acceleration
export NETFLIX_GPU=true

# Set output quality
export NETFLIX_QUALITY=high

# Set temporary directory
export NETFLIX_TEMP=/path/to/temp
```

## 📚 Examples

### Example 1: Basic Video Processing

```python
from netflix_food_cinematic_edit import CinematicEditor

editor = CinematicEditor()
editor.process_video(
    'cooking_video.mp4',
    'cinematic_output.mp4',
    preset='netflix_dark'
)
```

### Example 2: Batch Processing with Progress Tracking

```python
from netflix_food_cinematic_edit import CinematicEditor
import os

editor = CinematicEditor()
input_dir = './raw_footage'
output_dir = './edited_footage'

files = [f for f in os.listdir(input_dir) if f.endswith('.mp4')]

for i, filename in enumerate(files, 1):
    input_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, f'edited_{filename}')
    
    print(f"Processing {i}/{len(files)}: {filename}")
    editor.process_video(input_path, output_path, preset='warm_cinematic')
```

### Example 3: Custom Preset Creation

```python
from netflix_food_cinematic_edit.presets import PresetBuilder

# Create custom preset
preset = PresetBuilder('my_custom_preset')
preset.set_color_grade(
    shadows={'r': 20, 'g': 18, 'b': 25},
    midtones={'r': 0, 'g': 5, 'b': -5},
    highlights={'r': 10, 'g': 8, 'b': 5}
)
preset.set_brightness(8)
preset.set_contrast(12)
preset.set_saturation(15)
preset.save()

# Use the custom preset
editor = CinematicEditor()
editor.process_video('input.mp4', 'output.mp4', preset='my_custom_preset')
```

### Example 4: Image Processing with Custom Parameters

```python
from netflix_food_cinematic_edit import CinematicEditor

editor = CinematicEditor()
editor.process_image(
    'food_photo.jpg',
    'edited_photo.jpg',
    preset='vibrant_food',
    brightness=5,
    contrast=10,
    saturation=8
)
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue: FFmpeg not found

**Solution:**
```bash
# Windows
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg
```

Verify installation:
```bash
ffmpeg -version
```

#### Issue: Out of Memory during processing

**Solution:**
- Reduce output quality: `--quality low`
- Process smaller batches
- Increase system RAM or use GPU acceleration
- Check available disk space (need at least 2x video file size)

#### Issue: Slow processing

**Solution:**
- Enable GPU acceleration: `export NETFLIX_GPU=true`
- Reduce output resolution: `-r 1280x720`
- Reduce frame rate if applicable
- Check system resources (CPU, RAM, disk I/O)

#### Issue: Output quality is poor

**Solution:**
- Ensure input file quality is high
- Use `--quality high` option
- Try different presets
- Adjust brightness, contrast, and saturation parameters

#### Issue: Color grading looks incorrect

**Solution:**
- Try different presets
- Check input video color space
- Adjust individual parameters
- Review the preview before final processing

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure:
- Code follows PEP 8 style guide
- Tests are included for new features
- Documentation is updated
- Commit messages are descriptive

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙋 Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Documentation**: Check the `docs/` directory for detailed guides
- **Examples**: See the `examples/` directory for usage examples
- **Email**: Contact through GitHub profile

## 🎯 Roadmap

- [ ] Real-time preview interface (GUI)
- [ ] Advanced AI-powered color correction
- [ ] Support for 8K video processing
- [ ] Machine learning-based effect suggestions
- [ ] Plugin system for custom effects
- [ ] Web-based interface
- [ ] Mobile app integration

## 📊 Performance Notes

- **Video Processing**: ~30-60 minutes per hour of 1080p footage (depends on preset and hardware)
- **Image Processing**: ~1-5 seconds per image
- **Memory Usage**: 2-4GB for standard processing
- **Disk Space**: Requires 2-3x the size of source material for temporary files

## ✨ Credits

Created and maintained by Akane1221

Special thanks to the FFmpeg project and the open-source community for their incredible tools and libraries.

---

**Last Updated**: December 28, 2025

For the latest updates and information, visit the [GitHub repository](https://github.com/Akane1221/netflix-food-cinematic-edit).
