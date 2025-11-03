#!/usr/bin/env python3
"""
Test runner for RAG system
Run with: python tests/run_tests.py
"""
import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_tests():
    """Run all tests"""
    print("=== Running RAG System Tests ===")
    
    # Run unit tests
    print("\n--- Running Unit Tests ---")
    unit_result = pytest.main([
        "tests/unit/",
        "-v",
        "--tb=short"
    ])
    
    # Run integration tests  
    print("\n--- Running Integration Tests ---")
    integration_result = pytest.main([
        "tests/integration/", 
        "-v",
        "--tb=short"
    ])
    
    print(f"\n=== Test Summary ===")
    print(f"Unit Tests: {'PASS' if unit_result == 0 else 'FAIL'}")
    print(f"Integration Tests: {'PASS' if integration_result == 0 else 'FAIL'}")
    
    return unit_result == 0 and integration_result == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
