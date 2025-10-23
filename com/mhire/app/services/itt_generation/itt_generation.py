import logging
import base64
from google import genai
from google.genai import types
from com.mhire.app.config.config import Config

logger = logging.getLogger(__name__)

class ITTGeneration:
    def __init__(self):
        self.config = Config()
        self.client = genai.Client(api_key=self.config.gemini_api_key)
    
    async def analyze_image(self, image_data: str, mime_type: str, prompt: str) -> str:
        """
        Analyze image and generate description using Gemini 2.0 Flash (Vision)
        Args:
            image_data: Base64 encoded image string
            mime_type: Image MIME type
            prompt: Text prompt for image analysis
        Returns: Generated description
        """
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=prompt),
                        types.Part.from_bytes(
                            data=image_bytes,
                            mime_type=mime_type
                        )
                    ],
                ),
            ]
            
            response = self.client.models.generate_content(
                model=self.config.gemini_chat_vision_model,
                contents=contents
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            raise
