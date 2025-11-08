"""
Memory Manager - Handles vector store for agent context and project memory
Uses FAISS for local vector storage (or Pinecone for cloud)
"""
import numpy as np
from typing import List, Dict, Any, Optional
import json
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import settings
from utils.logger import logger

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("FAISS not available. Install with: pip install faiss-cpu")


class MemoryManager:
    """
    Manages vector embeddings and retrieval for agent context
    Stores and retrieves relevant context using semantic search
    """
    
    def __init__(self, dimension: int = 384):
        """
        Initialize memory manager
        
        Args:
            dimension: Dimension of embedding vectors (384 for all-MiniLM-L6-v2)
        """
        self.dimension = dimension
        self.use_faiss = settings.VECTOR_STORE_TYPE == "faiss" and FAISS_AVAILABLE
        self.memories = []  # List of memory dictionaries
        
        if self.use_faiss:
            # Initialize FAISS index
            self.index = faiss.IndexFlatL2(dimension)
            logger.info(f"Initialized FAISS index with dimension {dimension}")
        else:
            # Fall back to simple in-memory storage
            self.index = None
            logger.info("Using simple in-memory storage (FAISS not available)")
    
    def _get_embedding(self, text: str) -> np.ndarray:
        """
        Get embedding for text
        For MVP, we'll use a simple hash-based fake embedding
        In production, use sentence-transformers or OpenAI embeddings
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        # Simple fake embedding for MVP
        # In production: use sentence-transformers
        # from sentence_transformers import SentenceTransformer
        # model = SentenceTransformer('all-MiniLM-L6-v2')
        # return model.encode(text)
        
        # For now, create a deterministic fake embedding
        np.random.seed(hash(text) % (2**32))
        return np.random.randn(self.dimension).astype('float32')
    
    def add_memory(self, text: str, metadata: Dict[str, Any]) -> int:
        """
        Add a memory to the store
        
        Args:
            text: Text content to store
            metadata: Associated metadata (agent, task_type, timestamp, etc.)
            
        Returns:
            Memory ID
        """
        embedding = self._get_embedding(text)
        memory_id = len(self.memories)
        
        memory = {
            "id": memory_id,
            "text": text,
            "metadata": metadata,
            "embedding": embedding.tolist()
        }
        
        self.memories.append(memory)
        
        if self.use_faiss and self.index is not None:
            self.index.add(embedding.reshape(1, -1))
        
        logger.debug(f"Added memory {memory_id}: {text[:50]}...")
        return memory_id
    
    def search(self, query: str, top_k: int = 5, filter_metadata: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Search for relevant memories
        
        Args:
            query: Search query
            top_k: Number of results to return
            filter_metadata: Optional metadata filters
            
        Returns:
            List of relevant memories with similarity scores
        """
        query_embedding = self._get_embedding(query)
        
        if self.use_faiss and self.index is not None and len(self.memories) > 0:
            # FAISS search
            distances, indices = self.index.search(
                query_embedding.reshape(1, -1), 
                min(top_k, len(self.memories))
            )
            
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < len(self.memories):
                    memory = self.memories[idx].copy()
                    memory["similarity"] = float(1 / (1 + dist))  # Convert distance to similarity
                    
                    # Apply metadata filter if provided
                    if filter_metadata:
                        if all(memory["metadata"].get(k) == v for k, v in filter_metadata.items()):
                            results.append(memory)
                    else:
                        results.append(memory)
        else:
            # Simple cosine similarity search
            results = []
            for memory in self.memories:
                mem_embedding = np.array(memory["embedding"])
                similarity = np.dot(query_embedding, mem_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(mem_embedding)
                )
                
                # Apply metadata filter if provided
                if filter_metadata:
                    if not all(memory["metadata"].get(k) == v for k, v in filter_metadata.items()):
                        continue
                
                result = memory.copy()
                result["similarity"] = float(similarity)
                results.append(result)
            
            # Sort by similarity
            results.sort(key=lambda x: x["similarity"], reverse=True)
            results = results[:top_k]
        
        logger.debug(f"Found {len(results)} memories for query: {query[:50]}...")
        return results
    
    def get_context_for_agent(self, agent_name: str, task_type: str, limit: int = 3) -> str:
        """
        Get relevant context for an agent about to execute a task
        
        Args:
            agent_name: Name of the agent
            task_type: Type of task being executed
            limit: Maximum number of context items to retrieve
            
        Returns:
            Formatted context string
        """
        # Search for relevant past executions
        query = f"{agent_name} {task_type}"
        results = self.search(
            query, 
            top_k=limit,
            filter_metadata={"agent": agent_name}
        )
        
        if not results:
            return "No previous context available."
        
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(
                f"[Context {i}] {result['text']}\n"
                f"(Relevance: {result['similarity']:.2f})"
            )
        
        return "\n\n".join(context_parts)
    
    def clear_project_memory(self, project_id: int):
        """Clear all memories for a specific project"""
        self.memories = [
            m for m in self.memories 
            if m["metadata"].get("project_id") != project_id
        ]
        
        # Rebuild FAISS index
        if self.use_faiss and self.index is not None:
            self.index = faiss.IndexFlatL2(self.dimension)
            for memory in self.memories:
                embedding = np.array(memory["embedding"]).astype('float32')
                self.index.add(embedding.reshape(1, -1))
        
        logger.info(f"Cleared memories for project {project_id}")
    
    def save_to_disk(self, filepath: str = "memory_store.json"):
        """Save memories to disk"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(self.memories, f)
        
        logger.info(f"Saved {len(self.memories)} memories to {filepath}")
    
    def load_from_disk(self, filepath: str = "memory_store.json"):
        """Load memories from disk"""
        if not Path(filepath).exists():
            logger.warning(f"Memory file {filepath} not found")
            return
        
        with open(filepath, 'r') as f:
            self.memories = json.load(f)
        
        # Rebuild FAISS index
        if self.use_faiss and self.index is not None:
            self.index = faiss.IndexFlatL2(self.dimension)
            for memory in self.memories:
                embedding = np.array(memory["embedding"]).astype('float32')
                self.index.add(embedding.reshape(1, -1))
        
        logger.info(f"Loaded {len(self.memories)} memories from {filepath}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about stored memories"""
        agents = {}
        for memory in self.memories:
            agent = memory["metadata"].get("agent", "unknown")
            agents[agent] = agents.get(agent, 0) + 1
        
        return {
            "total_memories": len(self.memories),
            "dimension": self.dimension,
            "store_type": "faiss" if self.use_faiss else "simple",
            "memories_by_agent": agents
        }


# Global instance
memory_manager = MemoryManager()

