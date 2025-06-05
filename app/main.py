# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

# Import your services
from app.services import image_service
from app.services import llm_service
# from app.services import audio_service   # For ElevenLabs

load_dotenv()

app = FastAPI(title="AI Story Weaver")

# Mount the static directory for serving generated images
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
async def startup_event():
    print("Application startup: Loading models...")
    
    # Load Local LLM
    if hasattr(llm_service, 'load_local_llm') and hasattr(llm_service, 'initialize_story_chain'):
        llm_service.load_local_llm()
        llm_service.initialize_story_chain()
    else:
        print("Warning: LLM loading or chain initialization functions not found.")
    
    # Load Stable Diffusion Model
    print("Loading Stable Diffusion model...")
    sd_status = await image_service.download_and_load_model()
    if not sd_status["is_loaded"]:
        print(f"Warning: Failed to load Stable Diffusion model: {sd_status['error']}")
    else:
        print("Stable Diffusion model loaded successfully.")
    
    print("Model loading routines complete (or attempted).")

@app.get("/")
async def read_root():
    return {"message": "Welcome to AI Story Weaver!"}

@app.get("/health")
async def health_check():
    sd_status = image_service.get_model_status()
    
    llm_instance_status = False
    if hasattr(llm_service, 'llm_instance'):
        llm_instance_status = llm_service.llm_instance is not None
        
    story_chain_status = False
    if hasattr(llm_service, 'story_generation_chain'):
        story_chain_status = llm_service.story_generation_chain is not None

    models_loaded_status = {
        "sd_model": sd_status,
        "local_llm_ready": llm_instance_status,
        "story_chain_ready": story_chain_status
    }
    return {"status": "ok", "models": models_loaded_status}

# New endpoints for model management
@app.post("/models/sd/download")
async def download_sd_model(model_id: str = None):
    """
    Explicitly download and load the Stable Diffusion model.
    If model_id is not provided, uses the default model from .env
    """
    status = await image_service.download_and_load_model(model_id)
    if not status["is_loaded"]:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load model: {status['error']}"
        )
    return status

@app.get("/models/sd/status")
async def get_sd_model_status():
    """Get the current status of the Stable Diffusion model"""
    return image_service.get_model_status()

from .routers import stories
app.include_router(stories.router)