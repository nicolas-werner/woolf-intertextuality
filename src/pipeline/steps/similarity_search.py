from typing import Dict, Any
from rich.console import Console
from .base import PipelineStep
from src.embeddings.openai_embedder import OpenAIEmbedder
from pathlib import Path
from datetime import datetime

console = Console()


class SimilaritySearchStep(PipelineStep):
    """Step for finding similar passages"""

    def __init__(self, embedder: OpenAIEmbedder, top_k: int = 1):
        """Initialize with embedder and document store

        Args:
            embedder: OpenAI embedder instance
            top_k: Number of similar/dissimilar passages to return (default: 2)
        """
        self.embedder = embedder
        self.document_store = embedder.document_store
        self.top_k = top_k
        
        # Create logs directory if it doesn't exist
        self.log_dir = Path("data/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log_similarity_scores(self, query_text: str, all_docs: list, similar_docs: list, dissimilar_docs: list):
        """Log similarity scores and passages to a file"""
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        log_path = self.log_dir / f"similarity_scores_{timestamp}.txt"
        
        with open(log_path, "w", encoding="utf-8") as f:
            # Log query
            f.write(f"Query Text:\n{query_text}\n\n")
            
            # Log all scores in sorted order
            f.write("All Similarity Scores (sorted):\n")
            f.write("-" * 80 + "\n")
            for doc in sorted(all_docs, key=lambda x: x.score, reverse=True):
                f.write(f"Score: {doc.score:.4f}\n")
                f.write(f"Text: {doc.content[:200]}...\n")
                f.write("-" * 80 + "\n")
            
            # Log selected similar passages
            f.write("\nSelected Similar Passages:\n")
            f.write("=" * 80 + "\n")
            for doc in similar_docs:
                f.write(f"Score: {doc.score:.4f}\n")
                f.write(f"Text: {doc.content}\n")
                f.write("=" * 80 + "\n")
            
            # Log selected dissimilar passages
            f.write("\nSelected Dissimilar Passages:\n")
            f.write("=" * 80 + "\n")
            for doc in dissimilar_docs:
                f.write(f"Score: {doc.score:.4f}\n")
                f.write(f"Text: {doc.content}\n")
                f.write("=" * 80 + "\n")
            
            # Log statistics
            all_scores = [doc.score for doc in all_docs]
            f.write("\nStatistics:\n")
            f.write(f"Total documents: {len(all_docs)}\n")
            f.write(f"Score range: {min(all_scores):.4f} to {max(all_scores):.4f}\n")
            f.write(f"Mean score: {sum(all_scores)/len(all_scores):.4f}\n")

        console.log(f"[green]Similarity scores logged to {log_path}[/green]")

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Find both similar and dissimilar passages"""
        query_text: str = input_data["query_text"]
        query_embedding = self.embedder.embed_query(query_text)

        # Get similar documents
        similar_docs = self.document_store._query_by_embedding(
            query_embedding=query_embedding,
            filters={},
            top_k=self.top_k,
            return_embedding=True,
            scale_score=True,
        )

        # Get ALL documents by using a large limit
        # Using 10000 as a reasonable upper limit that should get all documents
        all_docs = self.document_store._query_by_embedding(
            query_embedding=query_embedding,
            filters={},
            top_k=10000,  # Large number to get all documents
            return_embedding=True,
            scale_score=True,
        )
        
        # Sort all documents by similarity score
        all_docs_sorted = sorted(all_docs, key=lambda x: x.score, reverse=True)
        
        # Get most dissimilar docs from the bottom of the sorted list
        dissimilar_docs = all_docs_sorted[-self.top_k:]

        # Log similarity scores and passages
        self.log_similarity_scores(query_text, all_docs_sorted, similar_docs, dissimilar_docs)

        for doc in similar_docs:
            if not hasattr(doc, "meta"):
                doc.meta = {}
            doc.meta["similarity_type"] = "similar"
            console.log(
                f"[cyan]Similar passage (score: {doc.score:.3f}): {doc.content[:100]}...[/cyan]"
            )

        for doc in dissimilar_docs:
            if not hasattr(doc, "meta"):
                doc.meta = {}
            doc.meta["similarity_type"] = "dissimilar"
            console.log(
                f"[yellow]Dissimilar passage (score: {doc.score:.3f}): {doc.content[:100]}...[/yellow]"
            )

        input_data["similar_documents"] = similar_docs + dissimilar_docs
        return input_data
