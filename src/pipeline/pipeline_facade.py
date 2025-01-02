from typing import List
from haystack import Document
from rich.console import Console
from .orchestrator import PipelineOrchestrator
from src.utils.token_counter import TokenCounter
from src.models.schemas import Analysis

console = Console()


class PipelineFacade:
    """Facade for the intertextuality analysis pipeline"""

    def __init__(self, token_counter: TokenCounter):
        self.orchestrator = PipelineOrchestrator(token_counter=token_counter)

    def index_documents(self, documents: List[Document]) -> None:
        """Index documents for similarity search"""
        self.orchestrator.execute({"documents": documents})

    def find_similar_passages(self, query_text: str) -> List[Document]:
        """Find both similar and dissimilar passages"""
        result = self.orchestrator.execute({"query_text": query_text})
        return result["similar_documents"]

    def analyze_similarity(self, query_text: str, doc: Document) -> Analysis:
        """Analyze the similarity between two passages."""
        result = self.orchestrator.execute({
            "query_text": query_text,
            "document": doc
        })
        
        # Since we're now getting the Analysis object directly, just return it
        return result
