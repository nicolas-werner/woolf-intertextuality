from typing import List, Dict, Any
from rich.console import Console
from openai import OpenAI

from src.config.settings import settings
from src.embeddings.openai_embedder import OpenAIEmbedder
from src.vector_store.qdrant_store import QdrantManager
from src.prompts.generator import PromptGenerator

from .steps.base import PipelineStep
from .steps.document_indexing import DocumentIndexingStep
from .steps.similarity_search import SimilaritySearchStep
from .steps.intertextual_analysis import IntertextualAnalysisStep

console = Console()

class PipelineOrchestrator:
    """Orchestrates the intertextuality analysis pipeline"""
    
    def __init__(self, use_scholarly_prompt: bool = True):
        # Initialize components
        self.vector_store = QdrantManager(
            embedding_dim=settings.embeddings.dimension
        )
        
        self.embedder = OpenAIEmbedder(
            document_store=self.vector_store.document_store
        )
        
        self.prompt_generator = PromptGenerator()
        template_name = "system_scholarly" if use_scholarly_prompt else "system_standard"
        self.system_prompt = self.prompt_generator.generate(template_name=template_name)
        
        self.client = OpenAI(api_key=settings.openai_api_key)
        
        # Initialize all possible pipeline steps
        self.indexing_step = DocumentIndexingStep(
            embedder=self.embedder,
            vector_store=self.vector_store
        )
        self.search_step = SimilaritySearchStep(
            embedder=self.embedder
        )
        self.analysis_step = IntertextualAnalysisStep(
            client=self.client,
            prompt_generator=self.prompt_generator,
            system_prompt=self.system_prompt
        )
    
    def execute(self, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the appropriate pipeline steps based on input data"""
        current_data = initial_data.copy()
        
        try:
            # Determine which steps to run based on input data
            if "documents" in current_data:
                # Document indexing flow
                current_data = self.indexing_step.execute(current_data)
                
            elif "query_text" in current_data and "top_k" in current_data:
                # Similarity search flow
                current_data = self.search_step.execute(current_data)
                
            elif "query_text" in current_data and "similar_document" in current_data:
                # Analysis flow
                current_data = self.analysis_step.execute(current_data)
                
            else:
                raise ValueError("Invalid input data for pipeline execution")
                
            return current_data
            
        except Exception as e:
            console.print(f"[red]Error in pipeline execution: {str(e)}[/red]")
            raise 