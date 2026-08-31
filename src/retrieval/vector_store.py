import chromadb
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, collection_name: str = "nlc_electrical_docs"):
        """Initializes the in-memory ChromaDB client for stability."""
        self.client = chromadb.Client()
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]) -> bool:
        """Adds chunks to ChromaDB, rejecting duplicate document hashes."""
        if not chunks:
            return False

        # Check existing hashes to prevent duplicate ingestion
        existing_metadatas = self.collection.get(include=["metadatas"])["metadatas"]
        existing_hashes = set(m.get("doc_hash") for m in existing_metadatas if m and "doc_hash" in m)
        
        new_hash = chunks[0]["doc_hash"]
        source_name = chunks[0]["source"]
        
        if new_hash in existing_hashes:
            logger.info(f"Document '{source_name}' (Hash: {new_hash}) already exists. Skipping insertion.")
            return False

        ids = [chunk["chunk_id"] for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [{"source": c["source"], "page": c["page"], "doc_hash": c["doc_hash"]} for c in chunks]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )
        logger.info(f"Added {len(chunks)} chunks for {source_name}.")
        return True

    def get_collection_count(self) -> int:
        """Returns the total number of text chunks in the database."""
        return self.collection.count()

    def get_uploaded_documents(self) -> List[str]:
        """Returns a list of unique document names currently in the database."""
        metadatas = self.collection.get(include=["metadatas"])["metadatas"]
        if not metadatas:
            return []
        sources = set(m.get("source") for m in metadatas if m and "source" in m)
        return sorted(list(sources))

    def clear_database(self):
        """Deletes all documents and resets the vector store."""
        try:
            self.client.delete_collection(self.collection_name)
        except ValueError:
            pass
        self.collection = self.client.get_or_create_collection(name=self.collection_name)
        logger.info("Knowledge base cleared.")

    def search(self, query_embedding: List[float], n_results: int = 5) -> List[Dict[str, Any]]:
        """Searches the vector database for the most relevant chunks."""
        if self.collection.count() == 0:
            return []
            
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, self.collection.count()),
            include=["documents", "metadatas"]
        )
        
        retrieved_chunks = []
        if results["documents"] and results["documents"][0]:
            for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
                retrieved_chunks.append({
                    "text": doc,
                    "source": meta.get("source", "Unknown"),
                    "page": meta.get("page", "Unknown")
                })
        return retrieved_chunks
