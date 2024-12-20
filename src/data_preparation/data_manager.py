from pathlib import Path
import json
from typing import List, Tuple
from haystack import Document
from rich.console import Console

from src.data_preparation.preprocessing import TextPreprocessor
from src.data_preparation.preprocessed_data_store import PreprocessedDataStore
from src.config.settings import settings
from src.embeddings.openai_embedder import OpenAIEmbedder

console = Console()

class DataManager:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.data_store = PreprocessedDataStore()
        self.embedder = OpenAIEmbedder(document_store=None)  # Only for embedding

    def prepare_odyssey_chunks(self) -> List[Document]:
        """Process The Odyssey text and save with embeddings"""
        output_path = settings.texts["odyssey"].processed_path
        
        # Always process if file doesn't exist
        if not Path(output_path).exists():
            console.log("Processing The Odyssey...")
            chunks = self.preprocessor.process_odyssey(
                settings.texts["odyssey"].raw_path
            )
            # Generate embeddings before saving
            chunks = self.embedder.embed_documents(chunks)
            self.data_store.save_chunks(chunks, output_path)
            return chunks
        
        # Load existing chunks with embeddings
        return self.data_store.load_chunks(output_path)

    def prepare_dalloway_queries(self) -> List[Document]:
        """Process Mrs Dalloway text into query chunks"""
        output_path = settings.texts["dalloway"].query_path
        
        # Always process if file doesn't exist
        if not Path(output_path).exists():
            console.log("Processing Mrs Dalloway for queries...")
            queries = self.preprocessor.get_dalloway_queries(
                settings.texts["dalloway"].raw_path
            )
            # Generate embeddings before saving
            queries = self.embedder.embed_documents(queries)
            self.data_store.save_chunks(queries, output_path)
            return queries
        
        # Load existing chunks with embeddings
        return self.data_store.load_chunks(output_path)

    def load_data(self) -> Tuple[List[Document], List[Document]]:
        """Load or create query chunks and Odyssey documents"""
        console.log("📚 Loading and preparing documents")
        
        # Process both texts
        odyssey_docs = self.prepare_odyssey_chunks()
        dalloway_queries = self.prepare_dalloway_queries()
        
        console.log(f"[bold green]✅ Loaded {len(odyssey_docs)} Odyssey chunks and {len(dalloway_queries)} Dalloway queries![/bold green]")
        
        return dalloway_queries, odyssey_docs
