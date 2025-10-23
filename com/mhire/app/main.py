import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from com.mhire.app.services.ai_chatbot.ai_chatbot_router import router as chatbot_router
from com.mhire.app.services.tti_generation.tti_generation_router import router as tti_router
from com.mhire.app.services.itt_generation.itt_generation_router import router as itt_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="AI Cognitive Workbench",
    description="Conversational AI with Text-to-Image and Image-to-Text capabilities",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chatbot_router)
app.include_router(tti_router)
app.include_router(itt_router)

@app.get("/")
async def root():
    return {
        "message": "AI Cognitive Workbench API",
        "status": "active",
        "endpoints": {
            "chat": "/api/v1/chat",
            "text_to_image": "/api/v1/tti/generate",
            "image_to_text": "/api/v1/itt/analyze"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
