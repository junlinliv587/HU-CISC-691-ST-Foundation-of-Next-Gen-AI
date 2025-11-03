# src/api/app.py
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import sys
import logging

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import config
from src.main import RAGPipeline

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Academic RAG System",
    description="Retrieval-Augmented Generation system for academic papers",
    version="1.0.0"
)

# Add CORS middleware to allow frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG pipeline
rag_pipeline = RAGPipeline()

# Pydantic models for request/response validation
class QueryRequest(BaseModel):
    question: str
    top_k: int = 5

class DocumentResponse(BaseModel):
    content: str
    metadata: Dict[str, Any]
    similarity_score: float

class QueryResponse(BaseModel):
    question: str
    answer: str
    relevant_documents: List[DocumentResponse]
    document_count: int

class IngestResponse(BaseModel):
    status: str
    message: str
    document_count: int

class SystemStatus(BaseModel):
    status: str
    vector_store: Dict[str, Any]
    config: Dict[str, Any]

# API endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Academic RAG System API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "status": "/status",
            "query": "/query (POST)",
            "ingest": "/ingest (POST)"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Academic RAG API"}

@app.get("/status", response_model=SystemStatus)
async def get_system_status():
    """Get system status and statistics"""
    try:
        status = rag_pipeline.get_system_status()
        return status
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the RAG system with a question"""
    try:
        logger.info(f"Received query: {request.question}")
        
        # Get relevant documents
        result = rag_pipeline.query(request.question, top_k=request.top_k)
        
        # For now, we'll just return the retrieved documents
        # In the next step, we'll add LLM to generate actual answers
        answer = f"Found {result['document_count']} relevant documents. This is a placeholder response."
        
        return QueryResponse(
            question=request.question,
            answer=answer,
            relevant_documents=result['relevant_documents'],
            document_count=result['document_count']
        )
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest", response_model=IngestResponse)
async def ingest_document(file: UploadFile = File(...)):
    """Ingest a PDF document into the system"""
    try:
        # Check if file is PDF
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Create temporary file path
        temp_dir = "data/raw"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.filename)
        
        # Save uploaded file
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        logger.info(f"Saved uploaded file to: {temp_path}")
        
        # Ingest document
        success = rag_pipeline.ingest_document(temp_path)
        
        if success:
            status = rag_pipeline.get_system_status()
            return IngestResponse(
                status="success",
                message=f"Document '{file.filename}' ingested successfully",
                document_count=status['vector_store']['document_count']
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to ingest document")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ingesting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest-path")
async def ingest_document_by_path(file_path: str):
    """Ingest a document from a local file path"""
    try:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        success = rag_pipeline.ingest_document(file_path)
        
        if success:
            status = rag_pipeline.get_system_status()
            return {
                "status": "success",
                "message": f"Document '{file_path}' ingested successfully",
                "document_count": status['vector_store']['document_count']
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to ingest document")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ingesting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
