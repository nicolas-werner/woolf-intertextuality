from haystack_integrations.document_stores.qdrant import QdrantDocumentStore
from haystack import Document
from typing import List
from rich.console import Console
from src.config.settings import settings

console = Console()


class QdrantManager:
    def __init__(self, embedding_dim: int = settings.embeddings.dimension):
        """Initialize QdrantManager"""
        self.document_store = QdrantDocumentStore(
            path=":memory:", 
            recreate_index=True,  
            return_embedding=True,
            wait_result_from_api=True,
            embedding_dim=embedding_dim,
        )

    def add_documents(self, documents: List[Document]):
        """Add documents to the store"""
        console.log("📚 Adding documents to vector store")
        self.document_store.write_documents(documents)
        console.log("[bold green]✅ Documents added successfully![/bold green]")
        return documents

    def search(self, query: str, top_k: int = 5) -> List[Document]:
        """Search for top k similar text chunks"""
        return self.document_store.query(query, top_k=top_k)
