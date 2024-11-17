from typing import List
from haystack import Document
from rich.console import Console

from .orchestrator import PipelineOrchestrator
from src.models.schemas import IntertextualAnalysis

console = Console()

class PipelineFacade:
    """Main interface for the intertextuality analysis pipeline"""
    
    def __init__(self, use_scholarly_prompt: bool = True):
        self.orchestrator = PipelineOrchestrator(
            use_scholarly_prompt=use_scholarly_prompt
        )
    
    def index_documents(self, documents: List[Document]):
        """Index documents for analysis"""
        return self.orchestrator.execute({
            "documents": documents
        })["embedded_documents"]
    
    def find_similar_passages(self, query_text: str, top_k: int = 5):
        """Find similar passages to analyze"""
        return self.orchestrator.execute({
            "query_text": query_text,
            "top_k": top_k
        })["similar_documents"]
    
    def analyze_similarity(self, query_text: str, similar_doc: Document) -> IntertextualAnalysis:
        """Analyze potential intertextual references"""
        return self.orchestrator.execute({
            "query_text": query_text,
            "similar_document": similar_doc
        })["analysis"] 