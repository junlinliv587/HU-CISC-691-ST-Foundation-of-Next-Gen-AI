# config.py
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the RAG application"""
    
    # Base paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    
    # Document processing
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50
    
    # Embedding model
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Vector database
    VECTOR_DB_PATH = os.path.join(BASE_DIR, "chroma_db")
    COLLECTION_NAME = "academic_papers"
    
    # API settings
    API_HOST = "0.0.0.0"
    API_PORT = 8000
    
    # LLM settings - Now using environment variables
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    
    # Performance settings
    MAX_RETRIEVAL_DOCS = 5
    TEMPERATURE = 0.1  # Lower temperature for more consistent academic responses

config = Config()
