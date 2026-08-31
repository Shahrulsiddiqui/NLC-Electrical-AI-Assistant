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

    def _build_safe_history(self, chat_history, prompt):
        """Forces strict User -> Model -> User sequence to prevent API freezing."""
        safe_history = []
        expected_role = "user"
        
        if chat_history:
            for msg in chat_history:
                content = str(msg.get("content", "")).strip()
                if not content:
                    continue
                    
                current_role = "model" if msg["role"] == "assistant" else "user"
                
                # Only add the message if it perfectly alternates
                if current_role == expected_role:
                    safe_history.append({"role": current_role, "parts": [content]})
                    expected_role = "user" if current_role == "model" else "model"
                    
        # If the history ends with a User message, drop it to make room for the new prompt
        if safe_history and safe_history[-1]["role"] == "user":
            safe_history.pop()
            
        safe_history.append({"role": "user", "parts": [prompt]})
        return safe_history

    def generate_response(self, prompt: str, chat_history: list = None) -> str:
        try:
            formatted_history = self._build_safe_history(chat_history, prompt)
            response = self.model.generate_content(formatted_history)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")
            return f"Error communicating with AI: {str(e)}"

    def generate_stream(self, prompt: str, chat_history: list = None):
        try:
            formatted_history = self._build_safe_history(chat_history, prompt)
            response = self.model.generate_content(formatted_history, stream=True)
            
            for chunk in response:
                try:
                    # Safely extract text; ignores chunks blocked by Gemini's safety filters
                    if chunk.text:
                        yield chunk.text
                except Exception:
                    continue
                    
        except Exception as e:
            logger.error(f"Gemini Streaming Error: {str(e)}")
            yield f"⚠️ **API Connection Error:** {str(e)}"
