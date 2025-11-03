#!/usr/bin/env python3
"""
FastAPI Server for Academic RAG System
Run with: python run_api.py
"""
import uvicorn
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.api.app import app
from config import config

if __name__ == "__main__":
    print("=== Starting Academic RAG API Server ===")
    print(f"API will be available at: http://{config.API_HOST}:{config.API_PORT}")
    print("Endpoints:")
    print("    - GET /health : Health check")
    print("    - GET /status : System status") 
    print("    - POST /query : Query the RAG system")
    print("    - POST /ingest : Upload and ingest PDF document")
    print("\nPress Ctrl+C to stop the server")

    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT
        # Remove reload=True for now to avoid warning
    )