import logging
from fastapi import APIRouter
from com.mhire.app.services.itt_generation.itt_generation import ITTGeneration
from com.mhire.app.services.itt_generation.itt_generation_schema import ITTRequest, ITTResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/itt",
    tags=["Image-to-Text Generation"]
)

itt_generation = ITTGeneration()

@router.post("/analyze", response_model=ITTResponse)
async def analyze_image(request: ITTRequest):
    """
    Analyze image and generate description using Gemini 2.5 Flash
    """
    try:
        description = await itt_generation.analyze_image(
            image_data=request.image_data,
            mime_type=request.mime_type,
            prompt=request.prompt
        )
        
        return ITTResponse(description=description)
        
    except Exception as e:
        logger.error(f"Error in ITT endpoint: {e}")
        raise
