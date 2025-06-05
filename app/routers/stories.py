from fastapi import APIRouter, HTTPException
from app.models.schemas import StoryPromptRequest, FullStoryResponse # Updated for full response
from app.services import llm_service
# , image_service, audio_service # We'll add these next

router = APIRouter(
    prefix="/stories",
    tags=["stories"] # For grouping in API docs
)

@router.post("/generate", response_model=FullStoryResponse)
async def create_story_endpoint(request: StoryPromptRequest):
    """
    Generates a story with text, an image, and audio narration.
    """
    print(f"Received prompt: {request.prompt}")

    # 1. Generate Story Text
    story_text = await llm_service.generate_story_text(request.prompt)
    if not story_text or "Sorry" in story_text: # Basic error check
        raise HTTPException(status_code=500, detail="Failed to generate story text.")
    print(f"Generated story text: {story_text[:100]}...") # Print first 100 chars

    # --- Placeholders for Image and Audio Generation ---
    # We will implement these services next. For now, they return None or dummy data.

    # 2. Generate Image (Placeholder - will be implemented in image_service.py)
    # For simplicity, let's use the original prompt for the image for now.
    # A better approach would be to derive an image prompt from the generated story.
    # image_url = await image_service.generate_image_from_text(story_text[:200]) # Use beginning of story for image prompt
    # print(f"Generated image URL: {image_url}")

    # 3. Generate Audio (Placeholder - will be implemented in audio_service.py)
    # audio_data_base64 = await audio_service.generate_audio_from_text(story_text)
    # if audio_data_base64:
    #     print(f"Generated audio data (first 20 chars of base64): {audio_data_base64[:20]}...")
    # else:
    #     print("Failed to generate audio data.")


    return FullStoryResponse(
        story_text=story_text,
        # image_url=image_url,
        # audio_data=audio_data_base64
    )