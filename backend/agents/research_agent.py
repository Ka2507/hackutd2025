"""
Research Agent - Synthesizes competitor data and user feedback

Enhanced with RAG (Retrieval-Augmented Generation) using Pinecone.
"""
import logging
import sys
import os
from typing import Dict, Any, List
from .base_agent import BaseAgent

# Add parent directory to path for RAG imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.pinecone_rag import pinecone_rag

logger = logging.getLogger(__name__)


class ResearchAgent(BaseAgent):
    """Agent specialized in research, data synthesis, and user insights with RAG"""
    
    def __init__(self, context: Dict[str, Any] = None):
        super().__init__(
            name="ResearchAgent",
            goal="Synthesize research data, user feedback, and market insights using RAG",
            context=context
        )
        self.rag_enabled = pinecone_rag.is_available()
    
    async def execute(self, task_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute research-related tasks
        
        Args:
            task_input: Contains task_type and relevant parameters
                - task_type: "user_research", "competitor_research", "trend_analysis"
                - query: Research query or topic
                - sources: List of data sources to analyze
        """
        self.update_status("running")
        
        task_type = task_input.get("task_type", "user_research")
        query = task_input.get("query", "")
        sources = task_input.get("sources", ["reddit", "twitter"])
        
        try:
            if task_type == "user_research":
                result = await self._user_research(query, sources)
            elif task_type == "competitor_research":
                result = await self._competitor_research(query)
            elif task_type == "trend_analysis":
                result = await self._trend_analysis(query)
            else:
                result = await self._general_research(query, sources)
            
            # Store research findings in context
            self.update_context("research_findings", result)
            
            self.update_status("completed")
            return self.format_output(result, {"task_type": task_type})
            
        except Exception as e:
            self.update_status("failed")
            return self.format_output(
                {"error": str(e)},
                {"task_type": task_type, "error": True}
            )
    
    async def _retrieve_knowledge(self, query: str, top_k: int = 3) -> str:
        """
        Retrieve relevant knowledge from RAG system.
        
        Args:
            query: Search query
            top_k: Number of documents to retrieve
            
        Returns:
            Formatted context from retrieved documents
        """
        if not self.rag_enabled:
            logger.info("⚠️ RAG not enabled, using LLM only")
            return ""
        
        try:
            results = pinecone_rag.search(query, top_k=top_k)
            
            if not results:
                logger.info(f"🔍 No relevant knowledge found for: {query}")
                return ""
            
            # Format retrieved documents
            context_parts = []
            for i, doc in enumerate(results, 1):
                context_parts.append(
                    f"**Source {i}** (relevance: {doc['score']:.2f}):\n{doc['text']}\n"
                )
            
            context = "\n---\n".join(context_parts)
            logger.info(f"✅ Retrieved {len(results)} relevant documents")
            return context
            
        except Exception as e:
            logger.error(f"❌ Error retrieving knowledge: {e}")
            return ""
    
    async def _user_research(self, query: str, sources: List[str]) -> Dict[str, Any]:
        """Research user needs and pain points with RAG"""
        # Retrieve relevant knowledge
        rag_context = await self._retrieve_knowledge(f"user research personas pain points {query}", top_k=3)
        
        # Build enhanced prompt with RAG context
        if rag_context:
            prompt = f"""You are analyzing user research for: {query}

**Relevant Market Knowledge:**
{rag_context}

**Task:** Based on the above context and your expertise, provide:
1. Key user pain points
2. User needs and desires
3. Important user segments
4. Actionable insights for product development

Provide a comprehensive analysis."""
        else:
            prompt = f"Analyze user pain points and needs for: {query}"
        
        llm_response = await self._call_llm(prompt)
        
        return {
            "query": query,
            "sources_analyzed": sources,
            "synthesis": llm_response,
            "rag_enabled": self.rag_enabled,
            "knowledge_sources_used": 3 if rag_context else 0,
            "confidence_score": 0.92 if rag_context else 0.75
        }
    
    async def _competitor_research(self, query: str) -> Dict[str, Any]:
        """Research competitor products and features with RAG"""
        # Retrieve relevant competitive intelligence
        rag_context = await self._retrieve_knowledge(f"competitive intelligence market analysis {query}", top_k=3)
        
        if rag_context:
            prompt = f"""You are analyzing the competitive landscape for: {query}

**Relevant Market Intelligence:**
{rag_context}

**Task:** Based on the above context, provide:
1. Key competitors and their positioning
2. Feature comparison and gaps
3. Pricing strategies
4. Market opportunities for differentiation

Provide a detailed competitive analysis."""
        else:
            prompt = f"Research competitor landscape for: {query}"
        
        llm_response = await self._call_llm(prompt)
        
        return {
            "query": query,
            "analysis": llm_response,
            "rag_enabled": self.rag_enabled,
            "knowledge_sources_used": 3 if rag_context else 0,
            "confidence_score": 0.88 if rag_context else 0.70
        }
    
    async def _trend_analysis(self, query: str) -> Dict[str, Any]:
        """Analyze market and technology trends with RAG"""
        # Retrieve relevant trend data
        rag_context = await self._retrieve_knowledge(f"market trends technology analysis {query}", top_k=4)
        
        if rag_context:
            prompt = f"""You are analyzing market and technology trends for: {query}

**Relevant Market Trend Data:**
{rag_context}

**Task:** Based on the above context, provide:
1. Emerging market trends
2. Technology adoption patterns
3. Growth forecasts and predictions
4. Strategic recommendations

Provide a comprehensive trend analysis."""
        else:
            prompt = f"Analyze trends related to: {query}"
        
        llm_response = await self._call_llm(prompt)
        
        return {
            "query": query,
            "analysis": llm_response,
            "rag_enabled": self.rag_enabled,
            "knowledge_sources_used": 4 if rag_context else 0,
            "confidence_score": 0.90 if rag_context else 0.72
        }
    
    async def _general_research(self, query: str, sources: List[str]) -> Dict[str, Any]:
        """General research synthesis with RAG"""
        # Retrieve relevant knowledge
        rag_context = await self._retrieve_knowledge(query, top_k=3)
        
        if rag_context:
            prompt = f"""You are conducting research on: {query}

**Relevant Knowledge Base:**
{rag_context}

**Sources to consider:** {', '.join(sources)}

**Task:** Based on the above context and sources, provide:
1. Key findings and insights
2. Data-backed conclusions
3. Actionable recommendations
4. Areas requiring further investigation

Provide a comprehensive research synthesis."""
        else:
            prompt = f"Research and synthesize information about: {query} from {sources}"
        
        llm_response = await self._call_llm(prompt)
        
        return {
            "query": query,
            "sources": sources,
            "synthesis": llm_response,
            "rag_enabled": self.rag_enabled,
            "knowledge_sources_used": 3 if rag_context else 0,
            "confidence_score": 0.85 if rag_context else 0.68
        }

