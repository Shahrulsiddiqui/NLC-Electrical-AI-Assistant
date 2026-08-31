import google.generativeai as genai
import os
import config
from src.ai.prompts import SYSTEM_INSTRUCTION
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing.")
            
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel(
            model_name=config.GEMINI_MODEL_NAME,
            system_instruction=SYSTEM_INSTRUCTION
        )

    def generate_response(self, prompt: str, chat_history: list = None) -> str:
        """Standard generation with strict role-alternation enforcement."""
        try:
            formatted_history = []
            last_role = None
            
            if chat_history:
                for msg in chat_history:
                    content = msg.get("content")
                    if content and str(content).strip():
                        role = "model" if msg["role"] == "assistant" else "user"
                        if role != last_role:
                            formatted_history.append({"role": role, "parts": [content]})
                            last_role = role
                            
            if last_role == "user":
                formatted_history.pop()
                    
            formatted_history.append({"role": "user", "parts": [prompt]})
            response = self.model.generate_content(formatted_history)
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")
            return f"Error communicating with AI: {str(e)}"

    def generate_stream(self, prompt: str, chat_history: list = None):
        """Streams the response while preventing User-User history crashes."""
        try:
            formatted_history = []
            last_role = None
            
            if chat_history:
                for msg in chat_history:
                    content = msg.get("content")
                    if content and str(content).strip():
                        role = "model" if msg["role"] == "assistant" else "user"
                        # Gemini STRICTLY requires User -> Model -> User. Ignore duplicates.
                        if role != last_role:
                            formatted_history.append({"role": role, "parts": [content]})
                            last_role = role
                            
            # If a previous assistant response failed, remove the orphaned user query
            if last_role == "user":
                formatted_history.pop()
                    
            formatted_history.append({"role": "user", "parts": [prompt]})
            
            response = self.model.generate_content(formatted_history, stream=True)
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            logger.error(f"Gemini Streaming Error: {str(e)}")
            yield f"⚠️ **API Error:** {str(e)}\n\nClear your chat history or refresh the page."
