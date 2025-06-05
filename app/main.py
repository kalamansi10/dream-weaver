# app/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Import your services
# from app.services import image_service as local_image_service # For Stable Diffusion
from app.services import llm_service as local_llm_service     # For Local LLM
# from app.services import audio_service                        # For ElevenLabs

load_dotenv()

app = FastAPI(title="AI Story Weaver")

@app.on_event("startup")
async def startup_event():
    print("Application startup: Loading models...")
    # if hasattr(local_image_service, 'load_sd_pipeline'): # Check if using local SD
    #     local_image_service.load_sd_pipeline()
    local_llm_service.load_local_llm() # Load the local LLM
    local_llm_service.initialize_story_chain() # Initialize the chain after LLM is loaded
    # audio_service doesn't need explicit loading currently
    print("Model loading routines complete (or attempted).")

@app.get("/")
async def read_root():
    return {"message": "Welcome to AI Story Weaver!"}

@app.get("/health")
async def health_check():
    models_loaded_status = {
        # "sd_pipeline_ready": hasattr(local_image_service, 'sd_pipeline') and local_image_service.sd_pipeline is not None,
        "local_llm_ready": local_llm_service.llm_instance is not None,
        "story_chain_ready": local_llm_service.story_generation_chain is not None
    }
    return {"status": "ok", "models": models_loaded_status}

from .routers import stories
app.include_router(stories.router)