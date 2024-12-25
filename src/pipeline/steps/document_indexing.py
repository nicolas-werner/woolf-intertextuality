from typing import Dict, Any, List
from haystack import Document
from rich.console import Console
from .base import PipelineStep
from src.embeddings.openai_embedder import OpenAIEmbedder
from src.vector_store.qdrant_store import QdrantManager

console = Console()


class DocumentIndexingStep(PipelineStep):
    """Step for embedding and indexing documents"""

    def __init__(self, embedder: OpenAIEmbedder, vector_store: QdrantManager):
        self.embedder = embedder
        self.vector_store = vector_store

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        documents: List[Document] = input_data["documents"]

        console.log("📚 Indexing documents")
        embedded_docs = self.embedder.embed_documents(documents)
        self.vector_store.add_documents(embedded_docs)
        console.log("[bold green]✅ Indexing complete![/bold green]")

        return {"embedded_documents": embedded_docs}
