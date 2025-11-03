import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import pytest
from src.vector_store.chroma_manager import ChromaDBManager

class TestVectorStore:
    """Unit tests for vector store components"""
    
    def test_chromadb_initialization(self):
        """Test ChromaDB manager can be initialized"""
        manager = ChromaDBManager("./test_db", "test_collection")
        assert manager is not None
        assert manager.collection_name == "test_collection"
    
    def test_collection_operations(self):
        """Test basic collection operations"""
        manager = ChromaDBManager("./test_db", "test_collection_ops")
        count = manager.get_collection_info()
        assert count >= 0  # Should not raise exception

if __name__ == "__main__":
    pytest.main([__file__])
