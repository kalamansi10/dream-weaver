from diffusers import StableDiffusionPipeline
import torch
import io
import base64
from fastapi.concurrency import run_in_threadpool
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import uuid
from datetime import datetime

load_dotenv()

# --- Global variable for the Stable Diffusion pipeline ---
sd_pipeline_cpu = None
model_status: Dict[str, Any] = {
    "is_loaded": False,
    "model_id": None,
    "error": None
}

MODEL_ID = "stabilityai/stable-diffusion-2-1"
IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "generated_images")

# Ensure the images directory exists
os.makedirs(IMAGES_DIR, exist_ok=True)

def get_model_status() -> Dict[str, Any]:
    """Returns the current status of the model loading"""
    return model_status

async def download_and_load_model(model_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Explicitly downloads and loads the Stable Diffusion model.
    Returns a status dictionary with the result.
    """
    global sd_pipeline_cpu, model_status
    
    # Reset status
    model_status = {
        "is_loaded": False,
        "model_id": model_id or MODEL_ID,
        "error": None
    }
    
    try:
        print(f"Downloading and loading Stable Diffusion model ({model_status['model_id']})...")
        print("This may take a few minutes and download several gigabytes if it's the first time.")

        # Load the model with authentication if HF_TOKEN is provided
        auth_token = os.getenv('HF_TOKEN')
        if auth_token:
            print("Using Hugging Face authentication token...")
            pipe = StableDiffusionPipeline.from_pretrained(
                model_status['model_id'],
                torch_dtype=torch.float32,  # Using float32 for CPU compatibility
                use_auth_token=auth_token
            )
        else:
            pipe = StableDiffusionPipeline.from_pretrained(
                model_status['model_id'],
                torch_dtype=torch.float32  # Using float32 for CPU compatibility
            )

        pipe = pipe.to("cpu")
        sd_pipeline_cpu = pipe
        model_status["is_loaded"] = True
        print("Stable Diffusion CPU pipeline loaded successfully.")
        return model_status

    except Exception as e:
        error_msg = f"Could not load Stable Diffusion pipeline: {str(e)}"
        print(f"CRITICAL: {error_msg}")
        model_status["error"] = error_msg
        sd_pipeline_cpu = None
        return model_status

async def generate_image_from_text_sd_cpu(text_prompt: str, num_inference_steps: int = 20) -> Dict[str, str]:
    """
    Generates an image using local Stable Diffusion on the CPU.
    Returns a dictionary containing:
    - base64_data: base64 encoded PNG image string
    - file_path: path to the saved image file
    """
    global sd_pipeline_cpu

    if not model_status["is_loaded"]:
        print("Stable Diffusion model is not loaded. Please download and load the model first.")
        return None

    if not text_prompt:
        print("No prompt provided for image generation.")
        return None

    try:
        print(f"Generating SD image on CPU for prompt (first 100 chars): {text_prompt[:100]}...")
        print(f"Using num_inference_steps: {num_inference_steps}")

        def sync_pipeline_call(prompt, steps):
            image = sd_pipeline_cpu(prompt=prompt, num_inference_steps=steps).images[0]
            return image

        image_result = await run_in_threadpool(sync_pipeline_call, text_prompt, num_inference_steps)

        if image_result is None:
            print("Image generation failed or returned None.")
            return None

        # Generate a unique filename using timestamp and UUID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"story_image_{timestamp}_{unique_id}.png"
        file_path = os.path.join(IMAGES_DIR, filename)

        # Save the image to disk
        image_result.save(file_path, format="PNG")
        print(f"Image saved to: {file_path}")

        # Convert the PIL Image to a base64 string
        buffered = io.BytesIO()
        image_result.save(buffered, format="PNG")
        img_str_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        print("CPU image generation successful.")
        return {
            "base64_data": f"data:image/png;base64,{img_str_base64}",
            "file_path": file_path
        }

    except Exception as e:
        print(f"Error during CPU Stable Diffusion image generation: {e}")
        import traceback
        traceback.print_exc()
        return None

# This will be the function imported and used by other parts of your app
generate_image_from_text = generate_image_from_text_sd_cpu