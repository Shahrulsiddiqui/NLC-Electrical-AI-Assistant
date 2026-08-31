    def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Adds chunks to ChromaDB, rejecting duplicate document hashes."""
        if not chunks:
            return

        # Check existing hashes to prevent duplicate ingestion
        existing_metadatas = self.collection.get(include=["metadatas"])["metadatas"]
        existing_hashes = set(m.get("doc_hash") for m in existing_metadatas if m and "doc_hash" in m)
        
        new_hash = chunks[0]["doc_hash"]
        source_name = chunks[0]["source"]
        
        if new_hash in existing_hashes:
            logger.info(f"Document '{source_name}' (Hash: {new_hash}) already exists. Skipping insertion.")
            return False # Indicate it was skipped

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
        return True # Indicate success
