from fastapi import APIRouter, HTTPException
from app.models.schemas import StoryPromptRequest, FullStoryResponse # Updated for full response
from app.services import llm_service, image_service  # Added image_service import
# , audio_service # We'll add this next

router = APIRouter(
    prefix="/stories",
    tags=["stories"] # For grouping in API docs
)

@router.post("/generate", response_model=FullStoryResponse)
async def create_story_endpoint(request: StoryPromptRequest):
    """
    Generates a story with text and an image.
    """
    print(f"Received prompt: {request.prompt}")

    # 1. Generate Story Text
    story_text = await llm_service.generate_story_text(request.prompt)
    if not story_text or "Sorry" in story_text: # Basic error check
        raise HTTPException(status_code=500, detail="Failed to generate story text.")
    print(f"Generated story text: {story_text[:100]}...") # Print first 100 chars

    # 2. Generate Image from the story text
    # Use the first 200 characters of the story as the image prompt
    # This gives enough context while staying within token limits
    image_prompt = f"Create a beautiful illustration for this story: {story_text[:200]}"
    image_result = await image_service.generate_image_from_text(image_prompt)
    
    image_url = None
    if image_result:
        image_url = image_result["base64_data"]
        print(f"Successfully generated image for story. Saved to: {image_result['file_path']}")
    else:
        print("Warning: Image generation failed, continuing without image")

    # --- Placeholders for Audio Generation ---
    # We will implement this service next. For now, it returns None.

    return FullStoryResponse(
        story_text=story_text,
        image_url=image_url,
        audio_data=None  # Audio generation not implemented yet
    )