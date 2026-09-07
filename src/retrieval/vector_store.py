import chromadb
import logging
import os
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, collection_name: str = "nlc_electrical_docs", persist_dir: str = "./chroma_db"):
        os.makedirs(persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]) -> bool:
        if not chunks:
            return False

        existing_metadatas = self.collection.get(include=["metadatas"])["metadatas"]
        existing_hashes = set(m.get("doc_hash") for m in existing_metadatas if m and "doc_hash" in m)
        
        if chunks[0]["doc_hash"] in existing_hashes:
            return False

        ids = [chunk["chunk_id"] for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [{"source": c["source"], "page": c["page"], "doc_hash": c["doc_hash"]} for c in chunks]

        self.collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)
        return True

    def get_collection_count(self) -> int:
        return self.collection.count()

    def get_uploaded_documents(self) -> List[str]:
        metadatas = self.collection.get(include=["metadatas"])["metadatas"]
        if not metadatas:
            return []
        return sorted(list(set(m.get("source") for m in metadatas if m and "source" in m)))

    def clear_database(self):
        try:
            self.client.delete_collection(self.collection_name)
        except ValueError:
            pass
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def search(self, query_embedding: List[float], initial_k: int = 15, final_k: int = 5) -> Dict[str, Any]:
        """Two-stage retrieval: Fetches broad candidates, filters via distance, and scores confidence."""
        if self.collection.count() == 0:
            return {"chunks": [], "confidence": "NONE"}

        # Stage 1: Candidate Retrieval
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(initial_k, self.collection.count()),
            include=["documents", "metadatas", "distances"]
        )
        
        retrieved_chunks = []
        if results["documents"] and results["documents"][0]:
            for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
                retrieved_chunks.append({
                    "text": doc,
                    "source": meta.get("source", "Unknown"),
                    "page": meta.get("page", "Unknown"),
                    "distance": dist
                })

        # Stage 2: Rerank and filter to Top K
        retrieved_chunks = sorted(retrieved_chunks, key=lambda x: x["distance"])[:final_k]

        # Evaluate Retrieval Confidence (Chroma L2 distance: lower is better)
        confidence = "LOW"
        if retrieved_chunks:
            best_score = retrieved_chunks[0]["distance"]
            if best_score <= 1.1: 
                confidence = "HIGH"

        return {"chunks": retrieved_chunks, "confidence": confidence}
