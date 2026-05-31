import time
import random
from typing import Optional, List, Dict, Any, Union


def generate_id(prefix: str = "") -> str:
    """Generates a unique ID."""
    return f"{prefix}_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"

def get_current_timestamp() -> str:
    """Returns current timestamp in ISO format."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def create_ai_video(video_path: str, script: str, base_img: str, mp3_path: str) -> Dict[str, Any]:
    """
    Create a video using AI. A string describing where the video was created.
    
    Args:
        video_path: The path where the video will be saved
        script: The script to be used for the video
        base_img: initial image for the video (optional)
        mp3_path: path to the mp3 file (optional)
    
    Returns:
        Dict containing operation results or error message
    """
    if not video_path or not script or not base_img or not mp3_path:
        return {"error": "Required parameter(s) missing: video_path, script, base_img, mp3_path"}
    
    return {
        "status": "success",
        "message": "create_ai_video executed successfully",
        "timestamp": get_current_timestamp(),
        "id": generate_id("item"),
    }

def create_meme_image(image_path: str, top_text: str, bottom_text: str) -> Dict[str, Any]:
    """
    Create a meme with top and bottom text. A string describing the created meme.
    
    Args:
        image_path: The path to the image file to use as the meme base
        top_text: The text to place at the top of the meme
        bottom_text: The text to place at the bottom of the meme
    
    Returns:
        Dict containing operation results or error message
    """
    if not image_path or not top_text or not bottom_text:
        return {"error": "Required parameter(s) missing: image_path, top_text, bottom_text"}
    
    return {
        "status": "success",
        "message": "create_meme_image executed successfully",
        "timestamp": get_current_timestamp(),
        "id": generate_id("item"),
    }

def fill_in_story_template(title: str, characters: List[str], setting: str, conflict: str, story: str) -> Dict[str, Any]:
    """
    Write a story based on given parameters. A story created with the given parameters.
    
    Args:
        title: The title of the story
        characters: The characters in the story
        setting: The setting of the story
        conflict: The conflict in the story
        story: The story itself
    
    Returns:
        Dict containing operation results or error message
    """
    if not title or not characters or not setting or not conflict or not story:
        return {"error": "Required parameter(s) missing: title, characters, setting, conflict, story"}
    
    return {
        "status": "success",
        "message": "fill_in_story_template executed successfully",
        "timestamp": get_current_timestamp(),
    }

def run_stable_diffusion_model(image_path: str, prompt: str) -> Dict[str, Any]:
    """
    Run a stable diffusion model. A message indicating if the model was run successfully or not.
    
    Args:
        image_path: The image file name to input to the model (can be empty, then the image will be generated from scratch
        prompt: The prompt to input to the model
    
    Returns:
        Dict containing operation results or error message
    """
    if not image_path or not prompt:
        return {"error": "Required parameter(s) missing: image_path, prompt"}
    
    return {
        "status": "success",
        "message": "run_stable_diffusion_model executed successfully",
        "timestamp": get_current_timestamp(),
    }
