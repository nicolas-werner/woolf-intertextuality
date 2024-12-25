from typing import List
from haystack import Document
from rich.console import Console
from .orchestrator import PipelineOrchestrator
from src.utils.token_counter import TokenCounter
from src.pipeline.steps.intertextual_analysis import IntertextualAnalysis

console = Console()

class PipelineFacade:
    """Facade for the intertextuality analysis pipeline"""
    
    def __init__(self, token_counter: TokenCounter):
        self.orchestrator = PipelineOrchestrator(token_counter=token_counter)
    
    def index_documents(self, documents: List[Document]) -> None:
        """Index documents for similarity search"""
        self.orchestrator.execute({
            "documents": documents
        })
    
    def find_similar_passages(self, query_text: str) -> List[Document]:
        """Find both similar and dissimilar passages"""
        result = self.orchestrator.execute({
            "query_text": query_text
        })
        return result["similar_documents"]
    
    def analyze_similarity(self, query_text: str, document: Document) -> IntertextualAnalysis:
        """Analyze similarity between query text and document"""
        try:
            result = self.orchestrator.execute({
                "query_text": query_text,
                "document": document
            })
            console.log(f"[cyan]Pipeline result: {result}[/cyan]")
            if "analysis" not in result:
                raise KeyError(f"Expected 'analysis' in result, got keys: {list(result.keys())}")
            return result["analysis"]
        except Exception as e:
            console.print(f"[red]Error in analyze_similarity: {str(e)}[/red]")
            raise 