from typing import Dict, Any
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

        query_embedding = self.embedder.embed_query(query_text)

        similar_docs = self.document_store._query_by_embedding(
            query_embedding=query_embedding,
            filters={},
            top_k=self.top_k,
            return_embedding=True,
            scale_score=True,
        )

        all_docs = self.document_store._query_by_embedding(
            query_embedding=query_embedding,
            filters={},
            top_k=None,  
            return_embedding=True,
            scale_score=True,
        )

        dissimilar_docs = sorted(all_docs, key=lambda x: x.score)[: self.top_k]

        for doc in similar_docs:
            if not hasattr(doc, "meta"):
                doc.meta = {}
            doc.meta["similarity_type"] = "similar"
            console.log(f"[cyan]Similar passage (score: {doc.score:.3f}): {doc.content[:100]}...[/cyan]")

        for doc in dissimilar_docs:
            if not hasattr(doc, "meta"):
                doc.meta = {}
            doc.meta["similarity_type"] = "dissimilar"
            console.log(f"[yellow]Dissimilar passage (score: {doc.score:.3f}): {doc.content[:100]}...[/yellow]")

        input_data["similar_documents"] = similar_docs + dissimilar_docs
        return input_data
