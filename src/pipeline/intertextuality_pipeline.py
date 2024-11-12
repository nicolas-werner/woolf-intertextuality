from haystack import Document
from rich.console import Console
from typing import List
from src.config.settings import settings
from openai import OpenAI

from src.embeddings.openai_embedder import OpenAIEmbedder
from src.vector_store.qdrant_store import QdrantManager
from src.prompts.intertextual_analysis import (
    get_analysis_prompt, 
    IntertextualAnalysis, 
    load_system_prompt
)

console = Console()

class IntertextualityPipeline:
    def __init__(self, use_scholarly_prompt: bool = True):
        # Initialize vector store
        self.vector_store = QdrantManager(
            embedding_dim=settings.embeddings.dimension
        )
        
        # Initialize embedder
        self.embedder = OpenAIEmbedder(
            document_store=self.vector_store.document_store
        )
        
        # Initialize LLM client and prompt
        self.system_prompt = load_system_prompt(scholarly=use_scholarly_prompt)
        self.client = OpenAI(api_key=settings.openai_api_key)

    def index_documents(self, documents: List[Document]):
        """Index documents"""
        console.log("📚 Indexing documents")
        # First embed any documents that need it
        embedded_docs = self.embedder.embed_documents(documents)
        # Add to vector store
        self.vector_store.add_documents(embedded_docs)
        console.log("[bold green]✅ Indexing complete![/bold green]")

    def find_similar_passages(self, query_text: str, top_k: int = 5):
        """Find similar passages"""
        console.log("🔎 Searching for similar passages")
        return self.embedder.find_similar(query_text, top_k=top_k)

    def analyze_similarity(self, query_text: str, similar_doc: Document) -> IntertextualAnalysis:
        """Analyze a potential intertextual reference using a LLM"""
        prompt = get_analysis_prompt(
            dalloway_text=query_text,
            odyssey_text=similar_doc.content,
            similarity_score=similar_doc.score
        )
        
        completion = self.client.beta.chat.completions.parse(
            model=settings.llm.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format=IntertextualAnalysis,
            temperature=settings.llm.temperature,
            max_tokens=settings.llm.max_tokens
        )
        
        return completion.choices[0].message.parsed
