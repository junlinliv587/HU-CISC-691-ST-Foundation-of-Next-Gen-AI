# src/embedding/embedder.py
import logging
from typing import List
import numpy as np
import os

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Generate embeddings for text chunks"""
    
    def __init__(self, model_type: str = "openai"):
        self.model_type = model_type
        
        if model_type == "openai":
            try:
                from openai import OpenAI
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY environment variable not set")
                self.client = OpenAI(api_key=api_key)
                self.model_name = "text-embedding-3-small"
                logger.info("Using OpenAI embeddings")
            except ImportError:
                logger.warning("OpenAI not available, falling back to dummy embeddings")
                self.model_type = "dummy"
        else:
            self.model_type = "dummy"
            logger.info("Using dummy embeddings for testing")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text chunk"""
        if self.model_type == "openai":
            try:
                response = self.client.embeddings.create(
                    model=self.model_name,
                    input=text
                )
                return response.data[0].embedding
            except Exception as e:
                logger.error(f"Error generating OpenAI embedding: {e}")
                logger.info("Falling back to dummy embeddings")
                return self._generate_dummy_embedding(text)
        else:
            return self._generate_dummy_embedding(text)
    
    def _generate_dummy_embedding(self, text: str) -> List[float]:
        """Generate a simple dummy embedding for testing"""
        # Create a simple hash-based "embedding" for testing
        import hashlib
        seed = int(hashlib.md5(text.encode()).hexdigest()[:8], 16)
        np.random.seed(seed)
        return np.random.randn(1536).tolist()  # Same dimension as OpenAI embeddings
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        
        logger.info(f"Generated {len(embeddings)} embeddings using {self.model_type} model")
        return embeddings

# Test the embedder
if __name__ == "__main__":
    # Test with dummy embeddings (no API key needed)
    embedder = EmbeddingGenerator(model_type="dummy")
    test_texts = ["Hello world", "This is a test document about AI"]
    
    embeddings = embedder.generate_embeddings_batch(test_texts)
    print("✅ Embedding generator created successfully!")
    print(f"Generated {len(embeddings)} embeddings")
    print(f"Embedding dimension: {len(embeddings[0])}")
    print("Note: Using dummy embeddings for testing. Set OPENAI_API_KEY for production use.")
