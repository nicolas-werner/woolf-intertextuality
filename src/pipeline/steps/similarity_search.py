from typing import Dict, Any, List
from haystack import Document
from rich.console import Console
from .base import PipelineStep
from src.embeddings.openai_embedder import OpenAIEmbedder

console = Console()

class SimilaritySearchStep(PipelineStep):
    """Step for finding similar passages"""
    
    def __init__(self, embedder: OpenAIEmbedder, top_k: int = 2):
        """Initialize with embedder and document store
        
        Args:
            embedder: OpenAI embedder instance
            top_k: Number of similar/dissimilar passages to return (default: 2)
        """
        self.embedder = embedder
        self.document_store = embedder.document_store
        self.top_k = top_k
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Find both similar and dissimilar passages"""
        query_text: str = input_data["query_text"]
        
        # Get embeddings for query
        query_embedding = self.embedder.embed_query(query_text)
        
        # Find most similar passages
        similar_docs = self.document_store._query_by_embedding(
            query_embedding=query_embedding,
            filters={},
            top_k=self.top_k,
            return_embedding=True,
            scale_score=True
        )
        
        # Find most dissimilar passages by getting more results and taking the least similar
        all_docs = self.document_store._query_by_embedding(
            query_embedding=query_embedding,
            filters={},
            top_k=self.top_k * 10,  # Get more docs to find dissimilar ones
            return_embedding=True,
            scale_score=True
        )
        
        # Sort by score ascending and take the most dissimilar ones
        dissimilar_docs = sorted(all_docs, key=lambda x: x.score)[:self.top_k]
        
        # Mark similarity type and ensure all metadata is present
        for doc in similar_docs:
            if not hasattr(doc, 'meta'):
                doc.meta = {}
            doc.meta['similarity_type'] = 'similar'
            
        for doc in dissimilar_docs:
            if not hasattr(doc, 'meta'):
                doc.meta = {}
            doc.meta['similarity_type'] = 'dissimilar'
            
        # Combine results
        input_data["similar_documents"] = similar_docs + dissimilar_docs
        return input_data 