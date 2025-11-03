# src/vector_store/chroma_manager.py
import chromadb
import logging
from typing import List, Dict, Any
import uuid

logger = logging.getLogger(__name__)

class ChromaDBManager:
    """Manage ChromaDB vector database operations"""
    
    def __init__(self, db_path: str, collection_name: str):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection_name = collection_name
        self.collection = self._get_or_create_collection()
    
    def _get_or_create_collection(self):
        """Get existing collection or create new one"""
        try:
            collection = self.client.get_collection(self.collection_name)
            logger.info(f"Loaded existing collection: {self.collection_name}")
        except Exception:
            collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Academic papers collection"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
        return collection
    
    def add_documents(self, documents: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Add documents with their embeddings to the database"""
        try:
            ids = [str(uuid.uuid4()) for _ in range(len(documents))]
            documents_content = [doc['content'] for doc in documents]
            metadatas = [doc['metadata'] for doc in documents]
            
            self.collection.add(
                embeddings=embeddings,
                documents=documents_content,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(documents)} documents to vector database")
            
        except Exception as e:
            logger.error(f"Error adding documents to vector database: {e}")
            raise
    
    def search_similar(self, query_embedding: List[float], top_k: int = 5):
        """Search for similar documents"""
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            return results
        except Exception as e:
            logger.error(f"Error searching vector database: {e}")
            raise
    
    def get_collection_info(self):
        """Get information about the collection"""
        return self.collection.count()

# Test the vector store
if __name__ == "__main__":
    # Test without actually adding data
    manager = ChromaDBManager("./test_chroma", "test_collection")
    print(f"Vector store manager created. Collection count: {manager.get_collection_info()}")
