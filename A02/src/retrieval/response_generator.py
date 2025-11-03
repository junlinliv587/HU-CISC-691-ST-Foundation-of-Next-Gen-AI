# src/retrieval/response_generator.py
import logging
from typing import List, Dict, Any
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """Generate responses using LLM based on retrieved documents"""
    
    def __init__(self, config):
        self.config = config
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = config.LLM_MODEL
        
    def generate_response(self, question: str, documents: List[Dict[str, Any]]) -> str:
        """Generate a response using LLM based on retrieved documents"""
        try:
            if not documents:
                return "I couldn't find any relevant information in the knowledge base to answer your question."
            
            # Prepare context from documents
            context = self._prepare_context(documents)
            
            # Create prompt
            prompt = self._create_prompt(question, context)
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an academic research assistant. Provide accurate, well-supported answers based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.TEMPERATURE,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I encountered an error while generating a response: {str(e)}"
    
    def _prepare_context(self, documents: List[Dict[str, Any]]) -> str:
        """Prepare context string from retrieved documents"""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source_info = f"Source: {doc['metadata'].get('source', 'Unknown')}"
            if 'page' in doc['metadata']:
                source_info += f", Page: {doc['metadata']['page']}"
            
            context_parts.append(f"Document {i} ({source_info}):\n{doc['content']}\n")
        
        return "\n".join(context_parts)
    
    def _create_prompt(self, question: str, context: str) -> str:
        """Create prompt for LLM"""
        return f"""Based on the following context from academic papers, please answer the question.

Context:
{context}

Question: {question}

Instructions:
1. Answer based ONLY on the provided context
2. If the context doesn't contain enough information, say so
3. Be precise and academic in your tone
4. Cite the sources when possible (e.g., "According to Document 1...")
5. Keep the response concise but informative

Answer:"""
    
    def evaluate_response_quality(self, question: str, response: str, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate the quality of the generated response"""
        try:
            evaluation_prompt = f"""
            Question: {question}
            Response: {response}
            Retrieved Documents Count: {len(documents)}
            
            Please evaluate this response on:
            1. Relevance to question (1-10)
            2. Use of provided context (1-10) 
            3. Clarity and coherence (1-10)
            4. Overall quality (1-10)
            
            Provide scores and brief reasoning.
            """
            
            evaluation = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an evaluation assistant. Provide honest, constructive feedback."},
                    {"role": "user", "content": evaluation_prompt}
                ],
                temperature=0.1,
                max_tokens=300
            )
            
            return {
                "evaluation": evaluation.choices[0].message.content,
                "documents_used": len(documents)
            }
            
        except Exception as e:
            logger.error(f"Error evaluating response: {e}")
            return {"error": str(e)}

# Test the response generator
if __name__ == "__main__":
    from config import config
    
    if not config.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY not set. Please add it to your .env file")
    else:
        generator = ResponseGenerator(config)
        test_question = "What is machine learning?"
        test_documents = [{
            'content': 'Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions without being explicitly programmed.',
            'metadata': {'source': 'test.pdf', 'page': 1}
        }]
        
        response = generator.generate_response(test_question, test_documents)
        print("✅ Response generator test:")
        print(f"Question: {test_question}")
        print(f"Response: {response}")
