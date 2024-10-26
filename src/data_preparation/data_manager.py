from pathlib import Path
from typing import List, Dict, Tuple
import json
from haystack import Document
from rich.console import Console
from src.utils.text_preprocessor import TextPreprocessor
from src.data_preparation.preprocessed_data_store import PreprocessedDataStore
from src.config.settings import settings

console = Console()

class DataManager:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.data_store = PreprocessedDataStore()

    def prepare_odyssey_chunks(self) -> None:
        """Process The Odyssey text and save with embeddings"""
        output_path = settings.texts["odyssey"].processed_path
        
        if not output_path.exists():
            console.log("Processing The Odyssey...")
            chunks = self.preprocessor.process_odyssey(
                settings.texts["odyssey"].raw_path
            )
            self.data_store.save_chunks(chunks, output_path)

    def prepare_dalloway_queries(self) -> None:
        """Process Mrs Dalloway text into query chunks"""
        output_path = settings.texts["dalloway"].query_path
        
        if not output_path.exists():
            console.log("Processing Mrs Dalloway for queries...")
            queries = self.preprocessor.get_dalloway_queries(
                settings.texts["dalloway"].raw_path
            )
            query_chunks = [{"content": query} for query in queries]
            self.data_store.save_chunks(query_chunks, output_path)

    def load_data(self) -> Tuple[List[str], List[Document]]:
        """Load query chunks and Odyssey documents"""

        self.prepare_odyssey_chunks()
        self.prepare_dalloway_queries()
        
        odyssey_docs = self.data_store.load_chunks(
            settings.texts["odyssey"].processed_path
        )
        
        dalloway_queries = []
        with open(settings.texts["dalloway"].query_path, 'r') as f:
            for line in f:
                chunk = json.loads(line)
                dalloway_queries.append(chunk['content'])
        
        return dalloway_queries, odyssey_docs
