import logging
from google import genai
from google.genai import types
from langchain.memory import ConversationBufferMemory
from com.mhire.app.config.config import Config

logger = logging.getLogger(__name__)

class AIChatbot:
    def __init__(self):
        self.config = Config()
        self.client = genai.Client(api_key=self.config.gemini_api_key)
        self.memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )
    
    async def process_chat(self, message: str) -> str:
        """Process chat message with conversation memory"""
        try:
            # Get conversation history
            history = self.memory.load_memory_variables({})
            chat_history = history.get("chat_history", [])
            
            # Build contents with history
            contents = []
            
            # Add previous messages
            for msg in chat_history:
                if hasattr(msg, 'type'):
                    role = "user" if msg.type == "human" else "model"
                    contents.append(
                        types.Content(
                            role=role,
                            parts=[types.Part.from_text(text=msg.content)]
                        )
                    )
            
            # Add current message
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=message)]
                )
            )
            
            # Generate response
            response = self.client.models.generate_content(
                model=self.config.gemini_chat_vision_model,
                contents=contents
            )
            
            ai_response = response.text
            
            # Save to memory
            self.memory.save_context(
                {"input": message},
                {"output": ai_response}
            )
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Error in chat processing: {e}")
            raise
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()
