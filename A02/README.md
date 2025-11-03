# Academic RAG System

A Retrieval-Augmented Generation (RAG) system that enhances LLM responses with domain-specific knowledge from academic papers. This project was developed as part of the CISC691-ST Next-Gen AI course assignment.


## 🚀 Features

- **Document Ingestion**: Process and index academic PDF papers
- **Intelligent Retrieval**: Find relevant information using vector similarity search  
- **AI-Powered Responses**: Generate context-aware answers using OpenAI GPT
- **RESTful API**: Easy-to-use HTTP interface with automatic documentation
- **Performance Monitoring**: Track query times and system metrics


## 🏗️ System Architecture

The system follows a modular RAG architecture:

1. **Document Processing**: PDF text extraction and chunking
2. **Vector Storage**: ChromaDB for efficient similarity search  
3. **Retrieval Engine**: Find relevant document chunks
4. **Response Generation**: OpenAI GPT for intelligent answers
5. **API Layer**: FastAPI for web interface

For detailed architecture, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).


## 📦 Installation

### Prerequisites
- Python 3.8+
- OpenAI API key

### Quick Start
```bash
# Clone and setup
git clone <repository-url>
cd A02

# Create virtual environment
python -m venv rag_env
source rag_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
echo "OPENAI_API_KEY=your_key_here" > .env

# Start server
python run_api.py
For detailed installation instructions, see docs/DEPLOYMENT.md.


## 🎯 Usage

### Starting the Server
```bash
python run_api.py
The API will be available at http://localhost:8000 with interactive documentation at http://localhost:8000/docs.


## 🧪 Testing

Run the test suite to verify everything works:

```bash
# Run all tests
python tests/run_tests.py

# Or run specific test types
pytest tests/unit/      # Unit tests
pytest tests/integration/ # Integration tests


## 📊 Performance

- **Document Ingestion**: 2-5 seconds per page
- **Query Response**: 1-3 seconds average
- **Vector Search**: < 100ms retrieval time


## 🔧 Configuration

Key configuration options in `config.py`:
- `CHUNK_SIZE`: Text chunk size (default: 512)
- `CHUNK_OVERLAP`: Chunk overlap (default: 50) 
- `MAX_RETRIEVAL_DOCS`: Maximum documents per query (default: 5)


## 📁 Project Structure
A02/
├── src/ # Source code
│ ├── api/ # FastAPI application
│ ├── document_loader/ # PDF processing
│ ├── embedding/ # Vector embeddings
│ ├── retrieval/ # Search and response
│ └── vector_store/ # ChromaDB management
├── tests/ # Test suites
├── docs/ # Documentation
├── data/ # Document storage
└── config.py # Configuration


## 📚 Documentation

- [System Architecture](docs/ARCHITECTURE.md) - Detailed design and components
- [API Specification](docs/API_SPECIFICATION.md) - Complete API documentation  
- [Deployment Guide](docs/DEPLOYMENT.md) - Installation and setup instructions


## 🛠️ Development

### Adding New Features
1. Follow the modular architecture pattern
2. Add unit tests for new components
3. Update documentation accordingly

### Code Style
- Use type hints for better code clarity
- Follow PEP 8 style guide
- Include docstrings for all functions and classes

## 📄 License

This project was developed for academic purposes as part of the CISC691-ST Next-Gen AI course.

## 🙏 Acknowledgments

- Built with FastAPI, ChromaDB, and OpenAI
- Course: CISC691-ST Foundation of Next-Gen AI
- Institution: Harrisburg University of Science and Technology
