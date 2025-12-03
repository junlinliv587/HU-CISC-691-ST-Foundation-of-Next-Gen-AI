"""
LLM Logging Assignment - Simplified Version
Author: Junlin Li
Course: HU-CISC-691-ST
"""

import logging
import json
import sys
import time
from datetime import datetime

# Setup logging
def setup_logging():
    logger = logging.getLogger('AssignmentLogger')
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
    console.setFormatter(console_format)
    
    # File handler
    file = logging.FileHandler('assignment.log', encoding='utf-8')
    file.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file.setFormatter(file_format)
    
    logger.addHandler(console)
    logger.addHandler(file)
    
    return logger

def main():
    print("=" * 50)
    print("LLM Logging Assignment")
    print("=" * 50)
    
    # Setup logger
    logger = setup_logging()
    logger.info("Starting assignment demonstration")
    
    # Test 1: Log a request
    request_data = {
        "timestamp": datetime.now().isoformat(),
        "prompt": "Hello, how are you?",
        "model": "mock-llama"
    }
    
    logger.info("Sending request to LLM")
    logger.debug(f"Request JSON: {json.dumps(request_data, indent=2)}")
    
    # Simulate processing
    time.sleep(1)
    
    # Test 2: Log a response
    response_data = {
        "timestamp": datetime.now().isoformat(),
        "response": "Hello! I'm doing well. How can I assist you today?",
        "duration": 1.0,
        "tokens": 12
    }
    
    logger.info("Received response from LLM")
    logger.debug(f"Response JSON: {json.dumps(response_data, indent=2)}")
    
    # Test 3: Show different log levels
    logger.debug("Debug message - only in file")
    logger.info("Info message - in console and file")
    logger.warning("Warning message - in console and file")
    logger.error("Error message - in console and file")
    
    print("\n" + "=" * 50)
    print("Assignment Requirements:")
    print("=" * 50)
    print("✓ Python logging module")
    print("✓ Console output (standard output)")
    print("✓ File output (assignment.log)")
    print("✓ Request logging")
    print("✓ Response logging")
    print("✓ CoPilot used for development")
    print("\nCheck 'assignment.log' for full JSON data")
    print("=" * 50)

if __name__ == "__main__":
    main()
