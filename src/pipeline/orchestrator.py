from typing import Dict, Any
from rich.console import Console
from openai import OpenAI

from src.config.settings import settings
from src.embeddings.openai_embedder import OpenAIEmbedder
from src.vector_store.qdrant_store import QdrantManager
from src.prompts.generator import PromptGenerator
from src.utils.token_counter import TokenCounter

from .steps.document_indexing import DocumentIndexingStep
from .steps.similarity_search import SimilaritySearchStep
from .steps.intertextual_analysis import IntertextualAnalysisStep

console = Console()


class PipelineOrchestrator:
    """Orchestrates the intertextuality analysis pipeline"""

    def __init__(self, token_counter: TokenCounter):
        self.vector_store = QdrantManager(embedding_dim=settings.embeddings.dimension)

        self.embedder = OpenAIEmbedder(document_store=self.vector_store.document_store)

        self.prompt_generator = PromptGenerator()
        self.system_prompt = self.prompt_generator.generate(
            template_name=settings.llm.prompt_template
        )

        self.client = OpenAI(api_key=settings.openai_api_key)

        self.indexing_step = DocumentIndexingStep(
            embedder=self.embedder, vector_store=self.vector_store
        )
        self.search_step = SimilaritySearchStep(embedder=self.embedder)
        self.analysis_step = IntertextualAnalysisStep(
            client=self.client,
            prompt_generator=self.prompt_generator,
            system_prompt=self.system_prompt,
            token_counter=token_counter,
        )

    def execute(self, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the appropriate pipeline steps based on input data"""
        current_data = initial_data.copy()

        try:
            if "documents" in current_data:
                current_data = self.indexing_step.execute(current_data)

            elif "query_text" in current_data and "document" in current_data:
                console.log("[cyan]Executing analysis step...[/cyan]")
                result = self.analysis_step.execute(current_data)
                console.log(f"[cyan]Analysis step result: {result}[/cyan]")
                current_data.update(result)

            elif "query_text" in current_data:
                current_data = self.search_step.execute(current_data)

            else:
                raise ValueError("Invalid input data for pipeline execution")

            return current_data

        except Exception as e:
            console.print(f"[red]Error in pipeline execution: {str(e)}[/red]")
            console.print(f"[red]Current data: {current_data}[/red]")
            raise
