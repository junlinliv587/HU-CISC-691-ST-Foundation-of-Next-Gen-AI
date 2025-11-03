# Academic RAG System Architecture

## System Overview

The Academic RAG (Retrieval-Augmented Generation) system is designed to enhance Large Language Model (LLM) responses with domain-specific knowledge from academic papers. It allows users to query a knowledge base of research papers and get accurate, context-aware answers.

## System Architecture Diagram
┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│ Document │ │ Processing │ │ Vector │
│ Ingestion │───▶│ Pipeline │───▶│ Database │
│ │ │ │ │ │
│ • PDF Loader │ │ • Text Chunking │ │ • ChromaDB │
│ • Text Extract │ │ • Embedding │ │ • Similarity │
│ • Format Support│ │ • Metadata │ │ • Indexing │
└─────────────────┘ └──────────────────┘ └─────────────────┘
│ │ │
▼ ▼ ▼
┌─────────────────┐ ┌──────────────────┐ ┌─────────────────┐
│ FastAPI │ │ Retrieval │ │ Response │
│ Interface │◀──▶│ Engine │◀──▶│ Generation │
│ │ │ │ │ │
│ • REST API │ │ • Vector Search │ │ • OpenAI GPT │
│ • Web Docs │ │ • Relevance │ │ • Prompt │
│ • File Upload │ │ • Ranking │ │ • Context │
└─────────────────┘ └──────────────────┘ └─────────────────┘
## Core Components

### 1. Document Processing Layer

**AcademicPDFLoader** (`src/document_loader/pdf_loader.py`)
- Extracts text from PDF academic papers
- Preserves document structure and metadata
- Handles page-by-page processing

**TextChunker** (`src/document_loader/chunker.py`) 
- Splits long documents into manageable chunks
- Uses recursive splitting (paragraphs → sentences)
- Maintains semantic coherence

**EmbeddingGenerator** (`src/embedding/embedder.py`)
- Converts text chunks to numerical vectors
- Supports both OpenAI embeddings and local models
- Handles batch processing for efficiency

### 2. Vector Storage Layer

**ChromaDBManager** (`src/vector_store/chroma_manager.py`)
- Manages persistent vector storage
- Handles collection creation and management
- Provides similarity search capabilities

### 3. Retrieval & Generation Layer

**DocumentRetriever** (`src/retrieval/retriever.py`)
- Coordinates the retrieval process
- Combines embedding and vector search
- Ranks results by relevance

**ResponseGenerator** (`src/retrieval/response_generator.py`)
- Generates AI responses using OpenAI GPT
- Incorporates retrieved context into prompts
- Provides response quality evaluation

### 4. API Layer

**FastAPI Application** (`src/api/app.py`)
- Provides RESTful API endpoints
- Handles file uploads and queries
- Includes automatic API documentation

**RAGPipeline** (`src/main.py`)
- Orchestrates the complete workflow
- Manages performance monitoring
- Provides system status information

## Data Flow

### Document Ingestion Process
1. **Upload**: User uploads PDF document via API
2. **Extraction**: PDFLoader extracts text and metadata
3. **Chunking**: TextChunker splits content into 512-token chunks
4. **Embedding**: EmbeddingGenerator converts chunks to vectors
5. **Storage**: ChromaDBManager stores vectors with metadata

### Query Processing Process
1. **Question**: User submits query via API
2. **Embedding**: Question is converted to vector
3. **Retrieval**: Similarity search finds relevant chunks
4. **Context**: Top chunks are combined with question
5. **Generation**: LLM generates answer based on context
6. **Response**: Structured response returned to user

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend Framework** | FastAPI | REST API development |
| **Vector Database** | ChromaDB | Vector storage and search |
| **Embedding Models** | OpenAI text-embedding-3-small | Text to vector conversion |
| **LLM** | OpenAI GPT-3.5-turbo | Response generation |
| **Document Processing** | PyPDF, LangChain | PDF text extraction |
| **Testing** | Pytest | Unit and integration tests |
| **Configuration** | python-dotenv | Environment management |

## File Structure
A02/
├── src/
│ ├── api/ # FastAPI application
│ ├── document_loader/ # PDF and text processing
│ ├── embedding/ # Vector embedding generation
│ ├── retrieval/ # Search and response logic
│ └── vector_store/ # ChromaDB management
├── tests/ # Unit and integration tests
├── data/ # Document storage
├── docs/ # Documentation
└── config.py # Configuration settings

## Design Decisions

1. **Modular Architecture**: Each component is isolated for easier testing and maintenance
2. **FastAPI Choice**: For automatic API documentation and async support
3. **ChromaDB Selection**: Lightweight, Python-native vector database
4. **OpenAI Integration**: Cloud-based for reliability and performance
5. **Configuration Management**: Centralized config with environment variables for security
