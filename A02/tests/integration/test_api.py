import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import pytest
from fastapi.testclient import TestClient
from src.api.app import app

class TestAPI:
    """Integration tests for API endpoints"""
    
    def setup_method(self):
        self.client = TestClient(app)
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'healthy'
    
    def test_status_endpoint(self):
        """Test system status endpoint"""
        response = self.client.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert 'vector_store' in data
        assert 'config' in data
    
    def test_query_endpoint(self):
        """Test query endpoint"""
        response = self.client.post(
            "/query",
            json={"question": "test question", "top_k": 3}
        )
        assert response.status_code == 200
        data = response.json()
        assert 'question' in data
        assert 'answer' in data

if __name__ == "__main__":
    pytest.main([__file__])
