# src/retrieval/retriever.py
import logging
from typing import List, Dict, Any
from src.embedding.embedder import EmbeddingGenerator
from src.vector_store.chroma_manager import ChromaDBManager

logger = logging.getLogger(__name__)

class DocumentRetriever:
    """Retrieve relevant documents based on queries"""
    
    def __init__(self, config):
        self.config = config
        self.embedder = EmbeddingGenerator(model_type="dummy")  # Use dummy for now
        self.vector_store = ChromaDBManager(
            db_path=config.VECTOR_DB_PATH,
            collection_name=config.COLLECTION_NAME
        )
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the vector database"""
        logger.info(f"Adding {len(documents)} documents to vector store")
        
        # Extract text content for embedding
        texts = [doc['content'] for doc in documents]
        
        # Generate embeddings
        embeddings = self.embedder.generate_embeddings_batch(texts)
        
        # Add to vector store
        self.vector_store.add_documents(documents, embeddings)
        
        logger.info(f"Successfully added {len(documents)} documents")
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant documents for a query"""
        logger.info(f"Retrieving documents for query: '{query}'")
        
        # Generate query embedding
        query_embedding = self.embedder.generate_embedding(query)
        
        # Search vector database
        results = self.vector_store.search_similar(query_embedding, top_k=top_k)
        
        # Format results
        retrieved_docs = []
        if results['documents']:
            for i in range(len(results['documents'][0])):
                retrieved_docs.append({
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'similarity_score': results['distances'][0][i] if results['distances'] else 0.0
                })
        
        logger.info(f"Retrieved {len(retrieved_docs)} documents")
        return retrieved_docs
    
    def get_stats(self):
        """Get statistics about the vector store"""
        count = self.vector_store.get_collection_info()
        return {"document_count": count}

# Test the retriever
if __name__ == "__main__":
    from config import config
    
    retriever = DocumentRetriever(config)
    print("✅ Document retriever created successfully!")
    print(f"Vector store stats: {retriever.get_stats()}")
    
    # Test with a sample query
    test_query = "artificial intelligence"
    results = retriever.retrieve(test_query, top_k=2)
    print(f"Test retrieval for '{test_query}': found {len(results)} results")
