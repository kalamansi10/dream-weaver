from pydantic import BaseModel
from typing import Optional

class StoryPromptRequest(BaseModel):
    prompt: str
    # We can add more options later, e.g., style, length
    # style: Optional[str] = None

class StoryTextResponse(BaseModel):
    story_text: str

# We'll expand this later for images and audio
class FullStoryResponse(BaseModel):
    story_text: str
    image_url: Optional[str] = None # Or base64 image data
    audio_data: Optional[str] = None # Base64 audio data

    