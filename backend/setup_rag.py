#!/usr/bin/env python3
"""
Setup script for Pinecone RAG system

Populates the Pinecone index with initial knowledge base.
"""
import sys
import os
import asyncio
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag.pinecone_rag import pinecone_rag
from rag.knowledge_base import get_all_knowledge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def setup_rag():
    """Setup and populate RAG system."""
    logger.info("🚀 Setting up Pinecone RAG system...")
    
    # Check if RAG is available
    if not pinecone_rag.is_available():
        logger.error("❌ Pinecone RAG is not available. Check your API keys.")
        return False
    
    # Get knowledge base
    knowledge = get_all_knowledge()
    logger.info(f"📚 Loaded {len(knowledge)} documents from knowledge base")
    
    # Populate Pinecone
    logger.info("🔄 Upserting documents to Pinecone...")
    success = pinecone_rag.upsert_documents(knowledge)
    
    if success:
        logger.info("✅ RAG system setup complete!")
        
        # Test search
        logger.info("\n🔍 Testing search functionality...")
        test_queries = [
            "AI product management market size",
            "user personas for product managers",
            "feature prioritization frameworks"
        ]
        
        for query in test_queries:
            logger.info(f"\n📝 Query: {query}")
            results = pinecone_rag.search(query, top_k=2)
            for i, result in enumerate(results, 1):
                logger.info(f"  Result {i}: {result['id']} (score: {result['score']:.2f})")
        
        return True
    else:
        logger.error("❌ Failed to populate Pinecone")
        return False


if __name__ == "__main__":
    asyncio.run(setup_rag())

