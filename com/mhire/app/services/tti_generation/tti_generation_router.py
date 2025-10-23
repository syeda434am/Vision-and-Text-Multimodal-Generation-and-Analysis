import logging
import base64
from fastapi import APIRouter
from com.mhire.app.services.tti_generation.tti_generation import TTIGeneration
from com.mhire.app.services.tti_generation.tti_generation_schema import TTIRequest, TTIResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/tti",
    tags=["Text-to-Image Generation"]
)

tti_generation = TTIGeneration()

@router.post("/generate", response_model=TTIResponse)
async def generate_image(request: TTIRequest):
    """
    Generate image from text prompt using Gemini 2.5 Flash
    """
    try:
        image_data, mime_type = await tti_generation.generate_image(request.prompt)
        
        # Convert bytes to base64 string for JSON response
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        return TTIResponse(
            image_data=image_base64,
            mime_type=mime_type,
            prompt=request.prompt
        )
        
    except Exception as e:
        logger.error(f"Error in TTI endpoint: {e}")
        raise
