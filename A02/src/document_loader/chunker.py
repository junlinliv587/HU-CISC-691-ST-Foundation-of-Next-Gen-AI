# src/document_loader/chunker.py
import re
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class TextChunker:
    """Split text into chunks for processing"""
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str) -> List[str]:
        """Split text into chunks using recursive splitting"""
        # First try to split by paragraphs
        chunks = self._split_by_paragraphs(text)
        
        # If chunks are still too large, split by sentences
        if max(len(chunk) for chunk in chunks) > self.chunk_size:
            chunks = self._split_by_sentences(text)
        
        return chunks
    
    def _split_by_paragraphs(self, text: str) -> List[str]:
        """Split text by paragraphs (double newlines)"""
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _split_by_sentences(self, text: str) -> List[str]:
        """Split text by sentences"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Chunk a list of documents"""
        chunked_documents = []
        
        for doc in documents:
            chunks = self.split_text(doc['content'])
            
            for i, chunk in enumerate(chunks):
                chunked_doc = {
                    'content': chunk,
                    'metadata': {
                        **doc['metadata'],
                        'chunk_id': i,
                        'total_chunks': len(chunks)
                    }
                }
                chunked_documents.append(chunked_doc)
        
        logger.info(f"Created {len(chunked_documents)} chunks from {len(documents)} documents")
        return chunked_documents

# Test the chunker
if __name__ == "__main__":
    chunker = TextChunker()
    test_text = "This is a test document. It has multiple sentences. We want to see how it gets chunked."
    chunks = chunker.split_text(test_text)
    print(f"Created {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {chunk}")
