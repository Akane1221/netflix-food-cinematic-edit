#!/usr/bin/env python3
"""
Netflix-style Cinematic Food Video Editor
A complete video editing suite using MoviePy and OpenCV for food images
with cinematic effects, color grading, zoom animations, and audio support.
"""

import os
import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional
from moviepy.editor import (
    ImageClip, concatenate_videoclips, AudioFileClip,
    CompositeVideoClip, VideoFileClip, TextClip, ColorClip
)
from moviepy.video.fx.resize import resize
from moviepy.video.io.ffmpeg_writer import FFMPEG_VideoWriter
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CinematicFoodEditor:
    """
    A comprehensive cinematic video editor for food images with Netflix-style effects.
    """

    def __init__(self, output_dir: str = "output", width: int = 1920, height: int = 1080):
        """
        Initialize the cinematic editor.
        
        Args:
            output_dir: Directory for output videos
            width: Video width in pixels (default 1920 for Full HD)
            height: Video height in pixels (default 1080 for Full HD)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.width = width
        self.height = height
        self.fps = 30
        logger.info(f"CinematicFoodEditor initialized: {width}x{height} @ {self.fps}fps")

    # ==================== Color Grading ====================

    def apply_lut_color_grading(self, image: np.ndarray, lut_type: str = "warm") -> np.ndarray:
        """
        Apply Look-Up Table (LUT) based color grading for cinematic look.
        
        Args:
            image: Input image (BGR format)
            lut_type: Type of LUT - 'warm', 'cool', 'vintage', 'noir'
        
        Returns:
            Color graded image
        """
        img_float = image.astype(np.float32) / 255.0
        
        if lut_type == "warm":
            # Warm, golden tones
            img_float[:, :, 2] = np.clip(img_float[:, :, 2] * 1.2, 0, 1)  # Red boost
            img_float[:, :, 1] = np.clip(img_float[:, :, 1] * 1.1, 0, 1)  # Green boost
            
        elif lut_type == "cool":
            # Cool, blue tones
            img_float[:, :, 0] = np.clip(img_float[:, :, 0] * 1.2, 0, 1)  # Blue boost
            img_float[:, :, 2] = np.clip(img_float[:, :, 2] * 0.9, 0, 1)  # Red reduce
            
        elif lut_type == "vintage":
            # Vintage/faded look
            img_float = np.clip(img_float * 0.95, 0, 1)
            img_float[:, :, 1] = np.clip(img_float[:, :, 1] * 0.95, 0, 1)
            # Add slight sepia
            img_float[:, :, 0] = np.clip(img_float[:, :, 0] * 0.85, 0, 1)
            
        elif lut_type == "noir":
            # High contrast noir
            img_gray = cv2.cvtColor((img_float * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
            img_float = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR).astype(np.float32) / 255.0
            img_float = np.clip(img_float ** 0.8, 0, 1)  # Increase contrast
        
        return (np.clip(img_float, 0, 1) * 255).astype(np.uint8)

    def apply_vignette(self, image: np.ndarray, intensity: float = 0.5) -> np.ndarray:
        """
        Apply vignette effect for dramatic cinematic look.
        
        Args:
            image: Input image
            intensity: Vignette intensity (0-1)
        
        Returns:
            Image with vignette effect
        """
        rows, cols = image.shape[:2]
        kernel_x = cv2.getGaussianKernel(cols, cols / 2)
        kernel_y = cv2.getGaussianKernel(rows, rows / 2)
        kernel = kernel_y * kernel_x.T
        mask = kernel / kernel.max()
        mask = (mask ** (1 - intensity)).astype(np.float32)
        
        image_float = image.astype(np.float32)
        for i in range(3):
            image_float[:, :, i] *= mask
        
        return np.clip(image_float, 0, 255).astype(np.uint8)

    def apply_shadow_highlights(self, image: np.ndarray, shadows: float = 1.2, 
                               highlights: float = 0.8) -> np.ndarray:
        """
        Adjust shadows and highlights for depth.
        
        Args:
            image: Input image
            shadows: Shadow boost factor (>1 brightens shadows)
            highlights: Highlights reduction factor (<1 darkens highlights)
        
        Returns:
            Image with adjusted shadows and highlights
        """
        img_float = image.astype(np.float32) / 255.0
        
        # Convert to LAB for better shadow/highlight adjustment
        img_lab = cv2.cvtColor((img_float * 255).astype(np.uint8), cv2.COLOR_BGR2LAB)
        img_lab = img_lab.astype(np.float32)
        
        # Boost shadows in L channel
        img_lab[:, :, 0] = np.where(
            img_lab[:, :, 0] < 128,
            np.clip(img_lab[:, :, 0] * shadows, 0, 255),
            np.clip(img_lab[:, :, 0] * highlights, 0, 255)
        )
        
        img_lab = img_lab.astype(np.uint8)
        return cv2.cvtColor(img_lab, cv2.COLOR_LAB2BGR)

    # ==================== Zoom & Ken Burns Effects ====================

    def create_ken_burns_effect(self, image: np.ndarray, duration: float = 3.0,
                               zoom_start: float = 1.0, zoom_end: float = 1.3,
                               pan_direction: str = "in") -> ImageClip:
        """
        Create a Ken Burns (zoom and pan) effect for cinematic movement.
        
        Args:
            image: Input image
            duration: Duration of the effect in seconds
            zoom_start: Starting zoom level
            zoom_end: Ending zoom level
            pan_direction: Direction of pan - 'in', 'out', 'left', 'right'
        
        Returns:
            MoviePy ImageClip with Ken Burns effect
        """
        def apply_zoom_pan(get_frame, t):
            # Calculate interpolation factor
            progress = t / duration
            current_zoom = zoom_start + (zoom_end - zoom_start) * progress
            
            # Get dimensions
            h, w = image.shape[:2]
            new_h, new_w = int(h * current_zoom), int(w * current_zoom)
            
            # Resize image for zoom effect
            zoomed = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
            
            # Calculate pan offset
            y_offset = max(0, (new_h - h) // 2)
            x_offset = max(0, (new_w - w) // 2)
            
            if pan_direction == "in":
                # Zoom in from edges
                offset = int((new_h - h) * progress / 2)
                y_offset = offset
                x_offset = int((new_w - w) * progress / 2)
            elif pan_direction == "left":
                x_offset = int((new_w - w) * progress)
            elif pan_direction == "right":
                x_offset = int((new_w - w) * (1 - progress))
            
            # Crop to output size
            cropped = zoomed[y_offset:y_offset + h, x_offset:x_offset + w]
            
            if cropped.shape[0] < h or cropped.shape[1] < w:
                # Pad if needed
                cropped = cv2.copyMakeBorder(
                    cropped, 0, h - cropped.shape[0], 0, w - cropped.shape[1],
                    cv2.BORDER_CONSTANT, value=(0, 0, 0)
                )
            
            return cropped
        
        clip = ImageClip(image).set_duration(duration)
        return clip.fl(apply_zoom_pan)

    def create_slider_effect(self, image: np.ndarray, duration: float = 3.0,
                            direction: str = "left_to_right") -> ImageClip:
        """
        Create a slider/pan effect across the image.
        
        Args:
            image: Input image
            duration: Duration in seconds
            direction: Pan direction
        
        Returns:
            ImageClip with slider effect
        """
        def apply_slider(get_frame, t):
            progress = t / duration
            h, w = image.shape[:2]
            
            if direction == "left_to_right":
                offset = int(w * 0.3 * progress)
            elif direction == "right_to_left":
                offset = int(w * 0.3 * (1 - progress))
            elif direction == "top_to_bottom":
                offset = int(h * 0.3 * progress)
            else:  # bottom_to_top
                offset = int(h * 0.3 * (1 - progress))
            
            if direction in ["left_to_right", "right_to_left"]:
                return np.roll(image, offset, axis=1)
            else:
                return np.roll(image, offset, axis=0)
        
        clip = ImageClip(image).set_duration(duration)
        return clip.fl(apply_slider)

    # ==================== Text Overlays ====================

    def create_text_overlay(self, text: str, duration: float = 3.0,
                           position: Tuple[str, str] = ("center", "center"),
                           fontsize: int = 100, color: str = "white",
                           font: str = "Arial-Bold", opacity: float = 1.0) -> TextClip:
        """
        Create a styled text overlay with cinematic appearance.
        
        Args:
            text: Text content
            duration: Duration in seconds
            position: Position tuple (horizontal, vertical)
            fontsize: Font size
            color: Text color (name or hex)
            font: Font name
            opacity: Text opacity (0-1)
        
        Returns:
            MoviePy TextClip
        """
        txt_clip = TextClip(
            text,
            fontsize=fontsize,
            font=font,
            color=color,
            method='caption',
            size=(self.width - 200, None)
        )
        txt_clip = txt_clip.set_duration(duration)
        txt_clip = txt_clip.set_opacity(opacity)
        txt_clip = txt_clip.set_position(position)
        
        return txt_clip

    def create_subtitle_overlay(self, text: str, duration: float = 3.0,
                               fontsize: int = 50) -> TextClip:
        """
        Create a subtitle-style text overlay at the bottom.
        
        Args:
            text: Subtitle text
            duration: Duration in seconds
            fontsize: Font size
        
        Returns:
            MoviePy TextClip positioned at bottom
        """
        return self.create_text_overlay(
            text,
            duration=duration,
            position=("center", "bottom"),
            fontsize=fontsize,
            color="white",
            opacity=0.9
        )

    # ==================== Audio Processing ====================

    def add_audio_to_video(self, video_clip, audio_path: str, 
                          volume: float = 1.0, start_time: float = 0.0) -> VideoFileClip:
        """
        Add audio to video with volume control.
        
        Args:
            video_clip: MoviePy video clip
            audio_path: Path to audio file
            volume: Audio volume multiplier (0-1)
            start_time: Audio start time in seconds
        
        Returns:
            Video clip with audio
        """
        try:
            audio_clip = AudioFileClip(audio_path)
            audio_clip = audio_clip.volume_multiplier(volume)
            audio_clip = audio_clip.set_start(start_time)
            
            # Ensure audio duration matches video
            if audio_clip.duration > video_clip.duration:
                audio_clip = audio_clip.subclipped(0, video_clip.duration)
            
            video_clip = video_clip.set_audio(audio_clip)
            logger.info(f"Audio added: {audio_path} (volume: {volume})")
            return video_clip
        except Exception as e:
            logger.error(f"Error adding audio: {e}")
            return video_clip

    def create_audio_fade(self, audio_path: str, fade_in: float = 0.0,
                         fade_out: float = 0.0) -> AudioFileClip:
        """
        Create audio with fade in/out effects.
        
        Args:
            audio_path: Path to audio file
            fade_in: Fade in duration in seconds
            fade_out: Fade out duration in seconds
        
        Returns:
            Processed AudioFileClip
        """
        audio = AudioFileClip(audio_path)
        
        if fade_in > 0:
            audio = audio.audio_fadein(fade_in)
        if fade_out > 0:
            audio = audio.audio_fadeout(fade_out)
        
        return audio

    # ==================== Image Processing ====================

    def prepare_image(self, image_path: str, color_grade: str = "warm",
                     vignette: bool = True) -> np.ndarray:
        """
        Prepare image with color grading and effects.
        
        Args:
            image_path: Path to image file
            color_grade: Type of color grading
            vignette: Apply vignette effect
        
        Returns:
            Processed image
        """
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Resize to output dimensions
        image = cv2.resize(image, (self.width, self.height), interpolation=cv2.INTER_LANCZOS4)
        
        # Apply color grading
        image = self.apply_lut_color_grading(image, color_grade)
        
        # Apply shadow/highlight adjustment
        image = self.apply_shadow_highlights(image, shadows=1.15, highlights=0.85)
        
        # Apply vignette
        if vignette:
            image = self.apply_vignette(image, intensity=0.4)
        
        logger.info(f"Image prepared: {image_path}")
        return image

    # ==================== Video Assembly ====================

    def create_image_sequence_video(self, image_paths: List[str], 
                                   duration_per_image: float = 3.0,
                                   transition: str = "fade",
                                   color_grade: str = "warm") -> VideoFileClip:
        """
        Create video from sequence of images with transitions.
        
        Args:
            image_paths: List of image file paths
            duration_per_image: Duration for each image
            transition: Transition type ('fade', 'zoom', 'slide')
            color_grade: Color grading type
        
        Returns:
            Compiled VideoFileClip
        """
        clips = []
        
        for image_path in image_paths:
            # Prepare image
            image = self.prepare_image(image_path, color_grade=color_grade)
            
            # Apply effect based on transition type
            if transition == "zoom":
                clip = self.create_ken_burns_effect(
                    image,
                    duration=duration_per_image,
                    zoom_end=1.2
                )
            elif transition == "slide":
                clip = self.create_slider_effect(
                    image,
                    duration=duration_per_image,
                    direction="left_to_right"
                )
            else:  # fade (default)
                clip = ImageClip(image).set_duration(duration_per_image)
            
            clips.append(clip)
        
        # Concatenate clips
        if transition == "fade":
            final = concatenate_videoclips(clips)
        else:
            final = concatenate_videoclips(clips, method="chain")
        
        logger.info(f"Video sequence created: {len(clips)} images, {transition} transition")
        return final

    def add_title_sequence(self, video: VideoFileClip, title: str,
                          subtitle: str = "", duration: float = 3.0) -> VideoFileClip:
        """
        Add opening title sequence to video.
        
        Args:
            video: Base video clip
            title: Main title text
            subtitle: Subtitle text
            duration: Title duration
        
        Returns:
            Video with title sequence
        """
        # Create title background (black)
        title_bg = ColorClip(size=(self.width, self.height), color=(0, 0, 0))
        title_bg = title_bg.set_duration(duration)
        
        # Create title text
        title_clip = self.create_text_overlay(
            title,
            duration=duration,
            position=("center", "center"),
            fontsize=150,
            color="white"
        )
        
        # Create subtitle if provided
        if subtitle:
            subtitle_clip = self.create_text_overlay(
                subtitle,
                duration=duration,
                position=("center", 0.65),
                fontsize=80,
                color="gold",
                opacity=0.8
            )
            title_seq = CompositeVideoClip([title_bg, title_clip, subtitle_clip])
        else:
            title_seq = CompositeVideoClip([title_bg, title_clip])
        
        # Concatenate title with video
        final = concatenate_videoclips([title_seq, video])
        logger.info(f"Title sequence added: {title}")
        return final

    def add_credits_sequence(self, video: VideoFileClip, credits_text: str,
                            duration: float = 5.0) -> VideoFileClip:
        """
        Add ending credits sequence.
        
        Args:
            video: Base video clip
            credits_text: Credits text (use newlines for multiple lines)
            duration: Credits duration
        
        Returns:
            Video with credits
        """
        # Create credits background
        credits_bg = ColorClip(size=(self.width, self.height), color=(0, 0, 0))
        credits_bg = credits_bg.set_duration(duration)
        
        # Create credits text
        credits_clip = self.create_text_overlay(
            credits_text,
            duration=duration,
            position=("center", "center"),
            fontsize=60,
            color="white"
        )
        
        credits_seq = CompositeVideoClip([credits_bg, credits_clip])
        
        # Concatenate video with credits
        final = concatenate_videoclips([video, credits_seq])
        logger.info("Credits sequence added")
        return final

    # ==================== Export ====================

    def export_video(self, video_clip: VideoFileClip, filename: str = "output.mp4",
                    codec: str = "libx264", preset: str = "medium",
                    audio_codec: str = "aac") -> str:
        """
        Export video with optimized settings.
        
        Args:
            video_clip: MoviePy video clip to export
            filename: Output filename
            codec: Video codec (default: libx264)
            preset: Encoding preset (ultrafast, fast, medium, slow, slower)
            audio_codec: Audio codec
        
        Returns:
            Path to exported video
        """
        output_path = self.output_dir / filename
        
        logger.info(f"Exporting video: {output_path}")
        logger.info(f"Settings: {self.width}x{self.height}, {self.fps}fps, {codec}")
        
        try:
            video_clip.write_videofile(
                str(output_path),
                fps=self.fps,
                codec=codec,
                audio_codec=audio_codec,
                preset=preset,
                verbose=False,
                logger=None
            )
            logger.info(f"Video exported successfully: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Export failed: {e}")
            raise

    # ==================== Complete Workflow ====================

    def create_cinematic_food_video(self, image_paths: List[str],
                                   audio_path: Optional[str] = None,
                                   title: str = "Food Cinematic",
                                   description: str = "",
                                   color_grade: str = "warm",
                                   duration_per_image: float = 3.0,
                                   output_filename: str = "cinematic_food.mp4") -> str:
        """
        Create a complete cinematic food video from scratch.
        
        Args:
            image_paths: List of food image paths
            audio_path: Optional path to background music
            title: Video title
            description: Video description/subtitle
            color_grade: Color grading type
            duration_per_image: Duration per image
            output_filename: Output video filename
        
        Returns:
            Path to exported video
        """
        logger.info("=" * 60)
        logger.info("Starting cinematic food video creation")
        logger.info("=" * 60)
        
        # Create image sequence
        video = self.create_image_sequence_video(
            image_paths,
            duration_per_image=duration_per_image,
            transition="zoom",
            color_grade=color_grade
        )
        
        # Add title sequence
        video = self.add_title_sequence(video, title, description, duration=3.0)
        
        # Add audio if provided
        if audio_path and os.path.exists(audio_path):
            video = self.add_audio_to_video(video, audio_path, volume=0.8)
        
        # Add credits
        credits = "Thank you for watching\n© Cinematic Food Edit"
        video = self.add_credits_sequence(video, credits, duration=3.0)
        
        # Export
        output_path = self.export_video(video, output_filename)
        
        logger.info("=" * 60)
        logger.info(f"Cinematic video completed: {output_path}")
        logger.info("=" * 60)
        
        return output_path


# ==================== CLI Usage ====================

def main():
    """Example usage of the cinematic editor."""
    
    # Initialize editor
    editor = CinematicFoodEditor(output_dir="output", width=1920, height=1080)
    
    # Example image paths (replace with actual paths)
    sample_images = [
        "food_image_1.jpg",
        "food_image_2.jpg",
        "food_image_3.jpg",
    ]
    
    # Check if sample images exist, create dummy message if not
    existing_images = [img for img in sample_images if os.path.exists(img)]
    
    if not existing_images:
        logger.warning("No sample images found. Please add food images to create a video.")
        logger.info("Usage example:")
        logger.info("  editor = CinematicFoodEditor()")
        logger.info("  video = editor.create_cinematic_food_video(")
        logger.info("      image_paths=['image1.jpg', 'image2.jpg'],")
        logger.info("      audio_path='background_music.mp3',")
        logger.info("      title='Delicious Food'")
        logger.info("  )")
        return
    
    # Create cinematic video
    try:
        output_path = editor.create_cinematic_food_video(
            image_paths=existing_images,
            title="Netflix Food Cinematic",
            description="A culinary journey in motion",
            color_grade="warm",
            duration_per_image=3.0,
            output_filename="netflix_food_cinematic.mp4"
        )
        print(f"\n✓ Video created successfully: {output_path}")
    except Exception as e:
        logger.error(f"Failed to create video: {e}")


if __name__ == "__main__":
    main()
