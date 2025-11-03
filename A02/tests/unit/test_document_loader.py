import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import pytest
from src.document_loader.pdf_loader import AcademicPDFLoader
from src.document_loader.chunker import TextChunker

class TestDocumentLoader:
    """Unit tests for document loading components"""
    
    def test_pdf_loader_initialization(self):
        """Test PDF loader can be initialized"""
        loader = AcademicPDFLoader()
        assert loader is not None
        assert '.pdf' in loader.supported_formats
    
    def test_chunker_initialization(self):
        """Test text chunker can be initialized"""
        chunker = TextChunker(chunk_size=512, chunk_overlap=50)
        assert chunker is not None
        assert chunker.chunk_size == 512
    
    def test_chunker_split_text(self):
        """Test text chunking functionality"""
        chunker = TextChunker()
        test_text = "This is sentence one. This is sentence two."
        chunks = chunker.split_text(test_text)
        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)

if __name__ == "__main__":
    pytest.main([__file__])
