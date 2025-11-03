import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import pytest
from src.main import RAGPipeline
from config import config

class TestRAGPipeline:
    """Integration tests for the complete RAG pipeline"""
    
    def test_pipeline_initialization(self):
        """Test that the RAG pipeline can be initialized"""
        pipeline = RAGPipeline()
        assert pipeline is not None
        assert hasattr(pipeline, 'loader')
        assert hasattr(pipeline, 'chunker')
        assert hasattr(pipeline, 'retriever')
    
    def test_system_status(self):
        """Test system status endpoint"""
        pipeline = RAGPipeline()
        status = pipeline.get_system_status()
        assert status['status'] == 'running'
        assert 'vector_store' in status
        assert 'config' in status
    
    def test_query_empty_database(self):
        """Test querying when no documents are ingested"""
        pipeline = RAGPipeline()
        result = pipeline.query("test query")
        assert 'question' in result
        assert 'document_count' in result
        assert result['document_count'] == 0  # No documents added yet

if __name__ == "__main__":
    pytest.main([__file__])
