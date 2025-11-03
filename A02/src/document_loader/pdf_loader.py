# src/document_loader/pdf_loader.py
import os
from typing import List, Dict, Any
from pypdf import PdfReader
import logging

logger = logging.getLogger(__name__)

class AcademicPDFLoader:
    """Loader for academic PDF papers"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def load_document(self, file_path: str) -> List[Dict[str, Any]]:
        """Load and extract text from PDF document"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            logger.info(f"Loading PDF: {file_path}")
            
            # Extract text from PDF
            reader = PdfReader(file_path)
            documents = []
            
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text.strip():  # Only add non-empty pages
                    documents.append({
                        'content': text,
                        'metadata': {
                            'source': file_path,
                            'page': page_num + 1,
                            'total_pages': len(reader.pages)
                        }
                    })
            
            logger.info(f"Extracted {len(documents)} pages from {file_path}")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {e}")
            raise

# Test the loader
if __name__ == "__main__":
    loader = AcademicPDFLoader()
    print("PDF loader created successfully!")
