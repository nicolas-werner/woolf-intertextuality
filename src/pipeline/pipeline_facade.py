from typing import List
from haystack import Document
from rich.console import Console

from .orchestrator import PipelineOrchestrator
from src.models.schemas import IntertextualAnalysis

console = Console()

class PipelineFacade:
    """Main interface for the intertextuality analysis pipeline"""
    
    def __init__(self):
        self.orchestrator = PipelineOrchestrator()
        self._analyzed_pairs = set()  # Track analyzed query-document pairs
    
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
        # Ensure document has an ID
        if not hasattr(similar_doc, 'id'):
            similar_doc.id = f"{similar_doc.meta.get('chapter', 'unknown')}_{id(similar_doc)}"
        
        # Create a unique key for this query-document pair
        pair_key = (query_text, similar_doc.id)
        
        # Check if this exact pair has been analyzed before
        if pair_key in self._analyzed_pairs:
            return similar_doc.analysis
        
        # Perform analysis
        analysis = self.orchestrator.execute({
            "query_text": query_text,
            "similar_document": similar_doc
        })["analysis"]
        
        # Cache the analysis
        similar_doc.analysis = analysis
        self._analyzed_pairs.add(pair_key)
        
        return analysis 