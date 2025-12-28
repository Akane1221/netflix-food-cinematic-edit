#!/usr/bin/env python3
"""
Project Initialization Script
Sets up project directories, configuration files, and provides FFmpeg installation instructions.
"""

import os
import sys
import platform
import subprocess
from pathlib import Path


# Define project directories
PROJECT_DIRS = {
    'images': 'Input images directory',
    'output': 'Output videos directory',
    'temp': 'Temporary processing files',
    'config': 'Configuration files',
    'logs': 'Log files'
}

# Sample config.yaml template
CONFIG_TEMPLATE = """# Netflix Food Cinematic Edit Configuration
# Last updated: 2025-12-28

project:
  name: "Food Cinematic Edit"
  version: "1.0.0"
  author: "Your Name"

video:
  output_format: "mp4"
  codec: "libx264"
  preset: "medium"  # Options: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
  crf: 23  # Quality (0-51, lower is better quality)
  fps: 30
  resolution: "1920x1080"
  bitrate: "5000k"

image_processing:
  enable_filter: true
  filter_type: "color_enhance"  # Options: color_enhance, blur, sharpen
  filter_strength: 1.0

audio:
  enabled: true
  source: "background"  # Options: background, input, none
  volume: 0.8
  fade_in_duration: 1.0
  fade_out_duration: 1.0

effects:
  enable_transitions: true
  transition_duration: 0.5
  transition_type: "fade"  # Options: fade, cross_fade, zoom, slide
  enable_text_overlay: false
  text_content: "Food Cinema"
  text_position: "bottom"

paths:
  input_dir: "./images"
  output_dir: "./output"
  temp_dir: "./temp"
  logs_dir: "./logs"

logging:
  level: "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
  enable_file_logging: true
  log_file: "project.log"
"""

# Sample images README
IMAGES_README = """# Images Directory

This directory contains the input images for video generation.

## Instructions:

1. Place your food/culinary images here
2. Supported formats: PNG, JPG, JPEG
3. Recommended specifications:
   - Resolution: 1920x1080 or higher
   - Color profile: sRGB
   - File size: < 10MB each

## Organization:

For best results, name your images in numerical or alphabetical order:
- image_001.jpg
- image_002.jpg
- image_003.jpg
- etc.

The video will be created in the order of file sorting.
"""

# FFmpeg installation instructions
FFMPEG_INSTRUCTIONS = {
    'Darwin': {
        'name': 'macOS',
        'brew': 'brew install ffmpeg',
        'instructions': [
            "FFmpeg Installation for macOS:",
            "================================",
            "",
            "Option 1 - Using Homebrew (Recommended):",
            "  1. Install Homebrew if not already installed:",
            "     /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"",
            "  2. Install FFmpeg:",
            "     brew install ffmpeg",
            "",
            "Option 2 - Using MacPorts:",
            "  sudo port install ffmpeg",
            "",
            "Verification:",
            "  ffmpeg -version"
        ]
    },
    'Linux': {
        'name': 'Linux',
        'instructions': [
            "FFmpeg Installation for Linux:",
            "================================",
            "",
            "Ubuntu/Debian:",
            "  sudo apt update",
            "  sudo apt install ffmpeg",
            "",
            "Fedora/RHEL:",
            "  sudo dnf install ffmpeg",
            "",
            "Arch Linux:",
            "  sudo pacman -S ffmpeg",
            "",
            "Verification:",
            "  ffmpeg -version"
        ]
    },
    'Windows': {
        'name': 'Windows',
        'instructions': [
            "FFmpeg Installation for Windows:",
            "==================================",
            "",
            "Option 1 - Using Chocolatey (Recommended):",
            "  1. Install Chocolatey if not already installed",
            "  2. Run in Command Prompt (Admin):",
            "     choco install ffmpeg",
            "",
            "Option 2 - Manual Installation:",
            "  1. Download from: https://ffmpeg.org/download.html",
            "  2. Extract to a folder (e.g., C:\\ffmpeg)",
            "  3. Add to PATH environment variable",
            "",
            "Option 3 - Using Windows Package Manager:",
            "  winget install FFmpeg",
            "",
            "Verification:",
            "  ffmpeg -version"
        ]
    }
}


def create_directories():
    """Create all required project directories."""
    print("\n📁 Creating project directories...")
    for dir_name, description in PROJECT_DIRS.items():
        dir_path = Path(dir_name)
        try:
            dir_path.mkdir(exist_ok=True)
            print(f"  ✓ Created: {dir_name}/ - {description}")
        except Exception as e:
            print(f"  ✗ Error creating {dir_name}/: {e}")
            return False
    return True


def create_config_file():
    """Create sample config.yaml file."""
    print("\n⚙️  Creating configuration template...")
    config_path = Path('config') / 'config.yaml'
    try:
        config_path.write_text(CONFIG_TEMPLATE)
        print(f"  ✓ Created: config/config.yaml")
        return True
    except Exception as e:
        print(f"  ✗ Error creating config file: {e}")
        return False


def create_images_readme():
    """Create README in images directory."""
    print("\n📝 Creating images directory README...")
    readme_path = Path('images') / 'README.md'
    try:
        readme_path.write_text(IMAGES_README)
        print(f"  ✓ Created: images/README.md")
        return True
    except Exception as e:
        print(f"  ✗ Error creating README: {e}")
        return False


def create_gitkeep_files():
    """Create .gitkeep files to preserve empty directories in git."""
    print("\n🔒 Creating .gitkeep files...")
    dirs_to_keep = ['temp', 'output', 'logs']
    for dir_name in dirs_to_keep:
        try:
            gitkeep_path = Path(dir_name) / '.gitkeep'
            gitkeep_path.touch()
            print(f"  ✓ Created: {dir_name}/.gitkeep")
        except Exception as e:
            print(f"  ✗ Error creating .gitkeep in {dir_name}: {e}")
            return False
    return True


def check_ffmpeg():
    """Check if FFmpeg is installed."""
    print("\n🎬 Checking FFmpeg installation...")
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  ✓ FFmpeg is installed: {version_line}")
            return True
    except FileNotFoundError:
        print("  ✗ FFmpeg is not installed")
        return False
    except Exception as e:
        print(f"  ✗ Error checking FFmpeg: {e}")
        return False


def display_ffmpeg_instructions():
    """Display FFmpeg installation instructions for the current OS."""
    system = platform.system()
    instructions = FFMPEG_INSTRUCTIONS.get(system)
    
    if instructions:
        print("\n" + "="*50)
        for line in instructions['instructions']:
            print(line)
        print("="*50)
    else:
        print("\nℹ️  FFmpeg installation guide:")
        print("  Visit: https://ffmpeg.org/download.html")


def create_main_gitignore():
    """Create a .gitignore file for the project root."""
    print("\n🚫 Creating .gitignore...")
    gitignore_content = """# Project-specific
temp/
output/
*.log
logs/*
!logs/.gitkeep

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Config with sensitive data
config/config_local.yaml
"""
    try:
        gitignore_path = Path('.gitignore')
        if not gitignore_path.exists():
            gitignore_path.write_text(gitignore_content)
            print(f"  ✓ Created: .gitignore")
        else:
            print(f"  ℹ️  .gitignore already exists")
        return True
    except Exception as e:
        print(f"  ✗ Error creating .gitignore: {e}")
        return False


def main():
    """Run all initialization steps."""
    print("\n" + "="*60)
    print("🚀 Netflix Food Cinematic Edit - Project Initialization")
    print("="*60)
    
    steps = [
        ("Directories", create_directories),
        ("Configuration", create_config_file),
        ("Images README", create_images_readme),
        ("Git Keep Files", create_gitkeep_files),
        ("Gitignore", create_main_gitignore),
    ]
    
    success_count = 0
    for step_name, step_func in steps:
        if step_func():
            success_count += 1
    
    print("\n" + "="*60)
    print(f"✅ Initialization Complete! ({success_count}/{len(steps)} steps successful)")
    print("="*60)
    
    # Check FFmpeg
    if not check_ffmpeg():
        print("\n⚠️  FFmpeg is required but not installed.")
        display_ffmpeg_instructions()
    
    print("\n📋 Next Steps:")
    print("  1. Add your food/cinematic images to the 'images/' directory")
    print("  2. Customize 'config/config.yaml' with your preferences")
    print("  3. Run your main processing script")
    print("\n💡 For more information, see README.md in the images directory")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Initialization cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
