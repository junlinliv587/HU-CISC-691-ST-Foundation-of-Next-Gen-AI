# src/main.py
import logging
import os
import sys
import time
from typing import List, Dict, Any

# Add the parent directory to Python path so we can import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config
from src.document_loader.pdf_loader import AcademicPDFLoader
from src.document_loader.chunker import TextChunker
from src.retrieval.retriever import DocumentRetriever
# from src.retrieval.response_generator import ResponseGenerator  # 暂时注释，没有API密钥

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RAGPipeline:
    """Complete RAG pipeline from document ingestion to response generation"""
    
    def __init__(self):
        self.config = config
        self.loader = AcademicPDFLoader()
        self.chunker = TextChunker(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )
        self.retriever = DocumentRetriever(config)
        # self.response_generator = ResponseGenerator(config)  # 暂时注释
        self.performance_stats = {
            "total_queries": 0,
            "average_retrieval_time": 0,
            "average_generation_time": 0
        }
    
    def ingest_document(self, file_path: str) -> bool:
        """Ingest a single document into the system"""
        try:
            logger.info(f"Starting ingestion of: {file_path}")
            
            # 1. Load document
            documents = self.loader.load_document(file_path)
            logger.info(f"Loaded {len(documents)} pages")
            
            # 2. Chunk documents
            chunked_documents = self.chunker.chunk_documents(documents)
            logger.info(f"Created {len(chunked_documents)} chunks")
            
            # 3. Add to vector store
            self.retriever.add_documents(chunked_documents)
            
            logger.info(f"Successfully ingested: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to ingest {file_path}: {e}")
            return False
    
    def query(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """Query the RAG system"""
        start_time = time.time()
        
        try:
            # 1. Retrieve relevant documents
            retrieval_start = time.time()
            relevant_docs = self.retriever.retrieve(question, top_k=top_k)
            retrieval_time = time.time() - retrieval_start
            
            # 2. Simple response without LLM
            if relevant_docs:
                answer = f"I found {len(relevant_docs)} relevant documents. To get AI-generated answers, please configure OpenAI API key."
            else:
                answer = "No relevant documents found. The system is working but no documents have been added yet."
            
            result = {
                "question": question,
                "answer": answer,
                "relevant_documents": relevant_docs,
                "document_count": len(relevant_docs),
                "performance": {
                    "retrieval_time_seconds": round(retrieval_time, 3),
                    "total_time_seconds": round(time.time() - start_time, 3)
                }
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error during query: {e}")
            return {"error": str(e)}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and statistics"""
        stats = self.retriever.get_stats()
        return {
            "status": "running",
            "vector_store": stats,
            "performance": self.performance_stats,
            "config": {
                "chunk_size": self.config.CHUNK_SIZE,
                "embedding_model": self.config.EMBEDDING_MODEL,
                "llm_model": "OpenAI GPT (API key not configured)",
                "max_retrieval_docs": self.config.MAX_RETRIEVAL_DOCS
            }
        }

def main():
    """Main function to demonstrate the RAG pipeline"""
    print("=== Academic RAG Pipeline Demo ===")
    
    # Initialize pipeline
    pipeline = RAGPipeline()
    
    # Show system status
    status = pipeline.get_system_status()
    print(f"System Status: {status}")
    
    print("\n✅ RAG Pipeline initialized successfully!")
    print("Current features:")
    print("  - Document ingestion and processing")
    print("  - Vector-based retrieval") 
    print("  - Performance monitoring")
    print("\nTo enable AI responses:")
    print("  1. Get OpenAI API key from https://platform.openai.com/api-keys")
    print("  2. Create .env file with: OPENAI_API_KEY=your_key_here")
    
    # Demo query
    demo_query = "What is machine learning?"
    print(f"\nTesting retrieval with query: '{demo_query}'")
    
    result = pipeline.query(demo_query)
    if "error" not in result:
        print(f"Answer: {result['answer']}")
        print(f"Performance: {result['performance']}")

if __name__ == "__main__":
    main()
