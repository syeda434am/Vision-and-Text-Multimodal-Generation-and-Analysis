import os
from dotenv import load_dotenv
            
load_dotenv()

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            # API settings
            cls._instance.gemini_api_key = os.getenv("GEMINI_API_KEY")
            cls._instance.gemini_chat_vision_model = os.getenv("GEMINI_CHAT_VISION_MODEL")
            cls._instance.gemini_image_model = os.getenv("GEMINI_IMAGE_MODEL")

        return cls._instance