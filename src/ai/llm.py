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
        """Fallback static response method."""
        try:
            formatted_history = []
            if chat_history:
                for msg in chat_history:
                    if msg.get("content"):  # Prevent empty history crashes
                        role = "model" if msg["role"] == "assistant" else "user"
                        formatted_history.append({"role": role, "parts": [msg["content"]]})
                    
            formatted_history.append({"role": "user", "parts": [prompt]})
            response = self.model.generate_content(formatted_history)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")
            return f"Error communicating with AI: {str(e)}"

    def generate_stream(self, prompt: str, chat_history: list = None):
        """Streams the response securely, catching silent chunk errors."""
        try:
            formatted_history = []
            if chat_history:
                for msg in chat_history:
                    # Never pass empty strings to Gemini; it causes silent crashes
                    if msg.get("content") and str(msg.get("content")).strip():
                        role = "model" if msg["role"] == "assistant" else "user"
                        formatted_history.append({"role": role, "parts": [msg["content"]]})
                    
            formatted_history.append({"role": "user", "parts": [prompt]})
            
            response = self.model.generate_content(formatted_history, stream=True)
            
            for chunk in response:
                try:
                    # Safely extract text. If Google blocks a chunk (safety rating), it skips smoothly.
                    if chunk.text:
                        yield chunk.text
                except Exception:
                    continue
                
        except Exception as e:
            logger.error(f"Gemini Streaming Error: {str(e)}")
            yield f"\n\n⚠️ **API Error:** {str(e)}"
