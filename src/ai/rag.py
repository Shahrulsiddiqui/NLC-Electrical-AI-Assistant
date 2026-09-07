from src.retrieval.embeddings import EmbeddingService
from src.retrieval.vector_store import VectorStore
from src.ai.llm import GeminiService
from src.ai.prompts import build_rag_prompt
from src.safety.guardrails import SafetyClassifier
from src.ai.query_router import QueryRouter
import logging

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        try:
            self.embedder = EmbeddingService()
            self.vector_store = VectorStore()
            self.llm = GeminiService()
            self.is_ready = True
        except Exception as e:
            logger.error(f"RAG init failed: {e}")
            self.is_ready = False
            self.error_msg = str(e)

    def stream_answer(self, query: str, chat_history: list) -> dict:
        if not self.is_ready:
            # Safely capture the string before yielding
            sys_err = self.error_msg
            def error_gen(): yield f"System error: {sys_err}"
            return {"generator": error_gen(), "sources": []}

        try:
            risk_level = SafetyClassifier.classify_query(query)
            query_type = QueryRouter.route_query(query)
            
            # Embed and Two-Stage Retrieve
            query_embedding = self.embedder.embed_query(query)
            search_results = self.vector_store.search(query_embedding)
            retrieved_chunks = search_results["chunks"]
            confidence = search_results["confidence"]
            
            # Build Context-Aware Prompt
            prompt = build_rag_prompt(query, retrieved_chunks, confidence)
            
            def response_generator():
                safety_prefix = SafetyClassifier.get_safety_disclaimer(risk_level)
                if safety_prefix:
                    yield safety_prefix + "\n\n"
                
                for chunk in self.llm.generate_stream(prompt, chat_history):
                    yield chunk

            return {
                "generator": response_generator(),
                "sources": retrieved_chunks
            }
            
        except Exception as e:
            # CRITICAL FIX: Save the error to a standard string variable first
            error_message = str(e)
            logger.error(f"RAG Error: {error_message}")
            
            def error_gen(): yield f"⚠️ **Error during retrieval:** {error_message}\n\nPlease check your API keys and try again."
            return {"generator": error_gen(), "sources": []}
