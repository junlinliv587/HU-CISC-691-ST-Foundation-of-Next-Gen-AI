# API Specification

## Base URL
http://localhost:8000

## Interactive Documentation
The API provides an interactive documentation interface at `/docs` where you can test endpoints directly.

## Endpoints

### Health Check
**GET /health**

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "Academic RAG API"
}