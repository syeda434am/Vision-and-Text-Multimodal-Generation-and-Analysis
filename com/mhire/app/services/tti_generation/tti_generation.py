import logging
import base64
from google import genai
from google.genai import types
from com.mhire.app.config.config import Config

logger = logging.getLogger(__name__)

class TTIGeneration:
    def __init__(self):
        self.config = Config()
        self.client = genai.Client(api_key=self.config.gemini_api_key)
    
    async def generate_image(self, prompt: str) -> tuple[bytes, str]:
        """
        Generate image from text prompt using Gemini 2.0 Flash Image
        Returns: (image_data, mime_type)
        """
        try:
            model = self.config.gemini_image_model
            
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=prompt),
                    ],
                ),
            ]
            
            generate_content_config = types.GenerateContentConfig(
                response_modalities=[
                    "IMAGE",
                    "TEXT",
                ],
            )
            
            image_data = None
            mime_type = None
            
            for chunk in self.client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if (
                    chunk.candidates is None
                    or chunk.candidates[0].content is None
                    or chunk.candidates[0].content.parts is None
                ):
                    continue
                
                if (chunk.candidates[0].content.parts[0].inline_data and 
                    chunk.candidates[0].content.parts[0].inline_data.data):
                    inline_data = chunk.candidates[0].content.parts[0].inline_data
                    image_data = inline_data.data
                    mime_type = inline_data.mime_type
                    break
            
            if image_data is None:
                raise ValueError("No image data generated")
            
            return image_data, mime_type
            
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            raise
