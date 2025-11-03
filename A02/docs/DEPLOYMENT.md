# Deployment Guide

## Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 1GB free space for documents and vectors
- **Operating System**: Linux, macOS, or Windows (WSL recommended for Windows)

### API Keys Required
- **OpenAI API Key**: For AI response generation ([Get one here](https://platform.openai.com/api-keys))

## Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone <your-repository-url>
cd A02

# Create and activate virtual environment
python -m venv rag_env
source rag_env/bin/activate  # On Windows: rag_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

