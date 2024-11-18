from typing import Dict, Any, List
from haystack import Document
from rich.console import Console
from .base import PipelineStep
from src.embeddings.openai_embedder import OpenAIEmbedder

console = Console()

class SimilaritySearchStep(PipelineStep):
    """Step for finding similar passages"""
    
    def __init__(self, embedder: OpenAIEmbedder):
        self.embedder = embedder
        self.top_k = 5  # Default value
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query_text: str = input_data["query_text"]
        top_k: int = input_data.get("top_k", self.top_k)  # Use input value or default
        
        console.log("🔎 Searching for similar passages")
        similar_docs = self.embedder.find_similar(
            query_text, 
            top_k=top_k
        )
        
        return {"similar_documents": similar_docs} 