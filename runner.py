#!/usr/bin/env python3
"""
Netflix Food Cinematic Video Creator
Main script to generate cinematic videos from food images
"""

import os
import sys
from pathlib import Path
from main import CinematicFoodEditor

def main():
    """Main execution function"""
    
    # Initialize editor
    editor = CinematicFoodEditor(output_dir="output", width=1920, height=1080)
    
    # Define image paths
    images_dir = Path("images")
    image_files = [
        images_dir / "image1.jpg",
        images_dir / "image2.jpg", 
        images_dir / "image3.jpg",
    ]
    
    # Check all images exist
    missing_images = [img for img in image_files if not img.exists()]
    if missing_images:
        print(f"❌ Missing images: {missing_images}")
        print("Please ensure all images are in the 'images/' directory")
        return
    
    print("=" * 60)
    print("🎬 Netflix Food Cinematic Video Creator")
    print("=" * 60)
    print(f"✓ Found {len(image_files)} images")
    
    # Create the cinematic video
    try:
        output_path = editor.create_cinematic_food_video(
            image_paths=[str(img) for img in image_files],
            audio_path=None,  # Add 'epic_music.mp3' if you have audio
            title="NETFLIX FOOD",
            description="CINEMATIC EXPERIENCE",
            color_grade="warm",
            duration_per_image=4.0,
            output_filename="netflix_food_cinematic.mp4"
        )
        
        print("\n" + "=" * 60)
        print(f"✅ SUCCESS! Video created at: {output_path}")
        print("=" * 60)
        print(f"Resolution: 1920x1080 @ 30fps")
        print(f"Format: MP4 (compatible with all players)")
        print("Ready to share! 🎉")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
