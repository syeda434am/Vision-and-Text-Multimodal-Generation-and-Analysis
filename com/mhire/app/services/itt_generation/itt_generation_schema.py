from pydantic import BaseModel, Field
from typing import Optional

class ITTRequest(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")
    mime_type: str = Field(default="image/jpeg", description="Image MIME type")
    prompt: Optional[str] = Field(default="Describe this image in detail.", description="Optional custom prompt")

class ITTResponse(BaseModel):
    description: str = Field(..., description="Generated image description")
