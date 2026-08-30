import google.generativeai as genai
import os
import config
from src.prompts import SYSTEM_INSTRUCTION
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing.")
            
        genai.configure(api_key=api_key)
        
        # Initialize model with system instruction
        self.model = genai.GenerativeModel(
            model_name=config.GEMINI_MODEL_NAME,
            system_instruction=SYSTEM_INSTRUCTION
        )

    def generate_response(self, prompt: str, chat_history: list = None) -> str:
        """
        Sends the formatted RAG prompt to Gemini along with conversation history.
        """
        try:
            # We don't use genai.ChatSession natively because we inject RAG context into the final prompt.
            # Instead, we pass the Streamlit history to establish memory.
            formatted_history = []
            if chat_history:
                for msg in chat_history:
                    # Map 'assistant' from Streamlit to 'model' for Gemini
                    role = "model" if msg["role"] == "assistant" else "user"
                    formatted_history.append({"role": role, "parts": [msg["content"]]})
                    
            # Add the current prompt as the latest user message
            formatted_history.append({"role": "user", "parts": [prompt]})
            
            response = self.model.generate_content(formatted_history)
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")
            return f"Error communicating with AI: {str(e)}"

