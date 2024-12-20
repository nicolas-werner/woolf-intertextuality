from haystack import Document
from haystack.components.embedders import OpenAITextEmbedder, OpenAIDocumentEmbedder
from typing import List, Dict
from src.config.settings import settings
from pathlib import Path
import numpy as np
from rich.console import Console

console = Console()

class OpenAIEmbedder:
    """Handles document embedding using OpenAI's embedding models."""
    
    def __init__(self, document_store=None):
        """Initialize embedder
        
        Args:
            document_store: Document store for storing and retrieving embeddings
        """
        self.document_store = document_store
        
        # Common configuration for embedders
        embedder_config = {
            "model": settings.embeddings.api_model
        }
        
        # Initialize embedders
        self.document_embedder = OpenAIDocumentEmbedder(**embedder_config)
        self.text_embedder = OpenAITextEmbedder(**embedder_config)
    
    def embed_documents(self, documents: List[Document]) -> List[Document]:
        """Embed documents that don't have embeddings"""
        docs_to_embed = []
        embedded_docs = []
        
        for doc in documents:
            if doc.embedding is not None:
                embedded_docs.append(doc)
                # console.log("[green]Using cached embedding[/green]")
            else:
                docs_to_embed.append(doc)
        
        if docs_to_embed:
            console.log(f"Embedding {len(docs_to_embed)} new documents...")
            newly_embedded = self.document_embedder.run(documents=docs_to_embed)
            embedded_docs.extend(newly_embedded["documents"])
        else:
            console.log("[bold green]All documents already have embeddings![/bold green]")
        
        return embedded_docs
    
    def find_similar(self, query: str, top_k: int = 5) -> List[Document]:
        """Find similar documents for a query"""
        query_result = self.text_embedder.run(text=query)
        similar_docs = self.document_store._query_by_embedding(
            query_embedding=query_result["embedding"],
            top_k=top_k,
            return_embedding=True,
            filters=None,
            scale_score=True
        )
        
        # Ensure each document has a unique ID
        for i, doc in enumerate(similar_docs):
            if not hasattr(doc, 'id'):
                doc.id = f"{doc.meta.get('chapter', 'unknown')}_{i}"
        
        return similar_docs
