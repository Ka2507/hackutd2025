"""
Pinecone RAG (Retrieval-Augmented Generation) Module

Handles vector storage, retrieval, and semantic search for the Research Agent.
"""
import logging
import sys
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import settings

logger = logging.getLogger(__name__)


class PineconeRAG:
    """RAG system using Pinecone for vector storage and retrieval."""
    
    def __init__(self):
        """Initialize Pinecone client and embedding model."""
        self.api_key = settings.pinecone_api_key
        self.environment = settings.pinecone_environment
        self.index_name = settings.pinecone_index_name
        
        self.pc = None
        self.index = None
        self.embedding_model = None
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
        
        if self.api_key:
            try:
                # Initialize Pinecone
                self.pc = Pinecone(api_key=self.api_key)
                
                # Initialize embedding model (lightweight and fast)
                logger.info("🔄 Loading embedding model (all-MiniLM-L6-v2)...")
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("✅ Embedding model loaded")
                
                # Create or connect to index
                self._setup_index()
                
                logger.info(f"✅ Pinecone RAG initialized | Index: {self.index_name}")
            except Exception as e:
                logger.error(f"❌ Error initializing Pinecone: {e}")
                self.pc = None
        else:
            logger.warning("⚠️ PINECONE_API_KEY not set. RAG features will be disabled.")
    
    def _setup_index(self):
        """Create or connect to Pinecone index."""
        try:
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                logger.info(f"🔄 Creating new Pinecone index: {self.index_name}")
                try:
                    self.pc.create_index(
                        name=self.index_name,
                        dimension=self.dimension,
                        metric='cosine',
                        spec=ServerlessSpec(
                            cloud='aws',
                            region=self.environment or 'us-east-1'
                        )
                    )
                    logger.info(f"✅ Index '{self.index_name}' created")
                except Exception as create_error:
                    if "ALREADY_EXISTS" in str(create_error):
                        logger.info(f"✅ Index '{self.index_name}' already exists, connecting...")
                    else:
                        raise create_error
            else:
                logger.info(f"✅ Connected to existing index: {self.index_name}")
            
            # Connect to index
            self.index = self.pc.Index(self.index_name)
            
            # Small delay to ensure connection
            import time
            time.sleep(1)
            
            # Check index stats
            stats = self.index.describe_index_stats()
            logger.info(f"📊 Index stats: {stats.total_vector_count} vectors")
            
        except Exception as e:
            logger.error(f"❌ Error setting up index: {e}")
            logger.info(f"📝 Attempting fallback connection to index...")
            try:
                # Try direct connection as fallback
                self.index = self.pc.Index(self.index_name)
                logger.info(f"✅ Fallback connection successful")
            except Exception as fallback_error:
                logger.error(f"❌ Fallback also failed: {fallback_error}")
                self.index = None
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        if not self.embedding_model:
            logger.error("❌ Embedding model not initialized")
            return []
        
        try:
            embedding = self.embedding_model.encode(text, convert_to_tensor=False)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"❌ Error generating embedding: {e}")
            return []
    
    def upsert_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """
        Store documents in Pinecone.
        
        Args:
            documents: List of documents with 'id', 'text', and 'metadata'
            
        Returns:
            Success status
        """
        if not self.index:
            logger.error("❌ Pinecone index not initialized")
            return False
        
        try:
            vectors = []
            for doc in documents:
                doc_id = doc.get('id')
                text = doc.get('text', '')
                metadata = doc.get('metadata', {})
                
                # Generate embedding
                embedding = self.embed_text(text)
                
                if embedding:
                    # Add text to metadata for retrieval
                    metadata['text'] = text
                    metadata['timestamp'] = datetime.now().isoformat()
                    
                    vectors.append({
                        'id': doc_id,
                        'values': embedding,
                        'metadata': metadata
                    })
            
            if vectors:
                self.index.upsert(vectors=vectors)
                logger.info(f"✅ Upserted {len(vectors)} documents to Pinecone")
                return True
            else:
                logger.warning("⚠️ No valid vectors to upsert")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error upserting documents: {e}")
            return False
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of matching documents with scores
        """
        if not self.index:
            logger.error("❌ Pinecone index not initialized")
            return []
        
        try:
            # Generate query embedding
            query_embedding = self.embed_text(query)
            
            if not query_embedding:
                return []
            
            # Search Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_metadata
            )
            
            # Format results
            documents = []
            for match in results.matches:
                documents.append({
                    'id': match.id,
                    'score': match.score,
                    'text': match.metadata.get('text', ''),
                    'metadata': {k: v for k, v in match.metadata.items() if k != 'text'}
                })
            
            logger.info(f"🔍 Found {len(documents)} relevant documents")
            return documents
            
        except Exception as e:
            logger.error(f"❌ Error searching Pinecone: {e}")
            return []
    
    def is_available(self) -> bool:
        """Check if RAG system is available."""
        return self.pc is not None and self.index is not None and self.embedding_model is not None


# Global RAG instance
pinecone_rag = PineconeRAG()

