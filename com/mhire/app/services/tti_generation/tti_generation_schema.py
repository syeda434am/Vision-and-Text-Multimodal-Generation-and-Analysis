from pydantic import BaseModel, Field

class TTIRequest(BaseModel):
    prompt: str = Field(..., description="Text prompt for image generation")

class TTIResponse(BaseModel):
    image_data: str = Field(..., description="Base64 encoded image data")
    mime_type: str = Field(..., description="Image MIME type")
    prompt: str = Field(..., description="Original prompt used")
