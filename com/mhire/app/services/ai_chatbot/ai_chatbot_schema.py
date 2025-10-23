from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI response")
