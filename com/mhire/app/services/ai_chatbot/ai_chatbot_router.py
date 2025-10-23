import logging
from fastapi import APIRouter
from com.mhire.app.services.ai_chatbot.ai_chatbot import AIChatbot
from com.mhire.app.services.ai_chatbot.ai_chatbot_schema import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["AI Chatbot"]
)

ai_chatbot = AIChatbot()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with AI using Gemini 2.5 Flash with conversation memory
    """
    try:
        response = await ai_chatbot.process_chat(request.message)
        return ChatResponse(response=response)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise

@router.delete("/clear")
async def clear_memory():
    """Clear conversation history"""
    try:
        ai_chatbot.clear_memory()
        return {"message": "Memory cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing memory: {e}")
        raise
