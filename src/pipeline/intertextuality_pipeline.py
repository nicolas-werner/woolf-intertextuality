from haystack import Pipeline
from haystack.schema import Document
from rich.console import Console
from typing import List
from src.config.settings import settings
from openai import OpenAI
import yaml

from src.embeddings.openai_embedder import OpenAIEmbeddingRetriever
from src.vector_store.qdrant_store import QdrantManager
from src.prompts.intertextual_analysis import (
    get_analysis_prompt, 
    IntertextualAnalysis, 
    load_system_prompt
)

console = Console()

class IntertextualityPipeline:
    def __init__(self):
        self.vector_store = QdrantManager(
            embedding_dim=settings.embeddings.dimension
        )
        
        self.embedder = OpenAIEmbeddingRetriever(
            document_store=self.vector_store.document_store
        )
        
        self.setup_pipelines()
        self.system_prompt = load_system_prompt()
        self.client = OpenAI(api_key=settings.openai_api_key)

    def setup_pipelines(self):
        """Initialize indexing and querying pipelines"""
        self.indexing = Pipeline()
        self.indexing.add_component("embedder", self.embedder)
        self.indexing.add_component("writer", self.vector_store.document_store)
        self.indexing.connect("embedder", "writer")
        
        self.querying = Pipeline()
        self.querying.add_component("retriever", self.embedder)

    def index_documents(self, documents: List[Document]):
        """Index documents"""
        console.log("📚 Indexing documents")
        self.indexing.run({"embedder": {"documents": documents}})
        console.log("[bold green]✅ Indexing complete![/bold green]")

    def find_similar_passages(self, query_text: str, top_k: int = 5):
        """Find similar passages"""
        console.log("🔎 Searching for similar passages")
        return self.querying.run({
            "retriever": {
                "query": query_text,
                "top_k": top_k
            }
        })["retriever"]["documents"]

    def analyze_similarity(self, query_text: str, similar_doc: Document) -> IntertextualAnalysis:
        """Analyze a potential intertextual reference using the LLM"""
        prompt = get_analysis_prompt(
            dalloway_text=query_text,
            odyssey_text=similar_doc.content,
            similarity_score=similar_doc.score
        )
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            response_model=IntertextualAnalysis,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response
