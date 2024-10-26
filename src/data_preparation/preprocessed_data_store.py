import json
from pathlib import Path
from typing import List, Dict, Union
from haystack import Document
import numpy as np
from rich.console import Console

console = Console()

class PreprocessedDataStore:
    def __init__(self, storage_type: str = "jsonl"):
        self.storage_type = storage_type
        
    def save_chunks(self, chunks: List[Dict], output_path: str) -> None:
        """Save preprocessed chunks with their metadata"""
        console.log(f"💾 Saving chunks to: {output_path}")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for chunk in chunks:
                # Convert numpy arrays to lists for JSON serialization if present
                if 'embedding' in chunk and isinstance(chunk['embedding'], np.ndarray):
                    chunk['embedding'] = chunk['embedding'].tolist()
                json.dump(chunk, f)
                f.write('\n')
        
        console.log(f"[bold green]✅ Saved {len(chunks)} chunks![/bold green]")
    
    def load_chunks(self, input_path: str) -> Union[List[str], List[Document]]:
        """Load preprocessed chunks. Returns Documents for Odyssey, strings for Dalloway"""
        console.log(f"📖 Loading chunks from: {input_path}")
        
        if 'dalloway' in input_path:
            # For Dalloway queries, just return the content
            queries = []
            with open(input_path, 'r', encoding='utf-8') as f:
                for line in f:
                    chunk = json.loads(line)
                    queries.append(chunk['content'])
            console.log(f"[bold green]✅ Loaded {len(queries)} query chunks![/bold green]")
            return queries
        else:
            # For Odyssey, return full Documents
            documents = []
            with open(input_path, 'r', encoding='utf-8') as f:
                for line in f:
                    chunk = json.loads(line)
                    if 'embedding' in chunk:
                        chunk['embedding'] = np.array(chunk['embedding'])
                    documents.append(Document(
                        content=chunk['content'],
                        meta=chunk.get('metadata', {}),
                        embedding=chunk.get('embedding')
                    ))
            console.log(f"[bold green]✅ Loaded {len(documents)} document chunks![/bold green]")
            return documents

    def merge_files(self, input_paths: List[str], output_path: str) -> None:
        """Merge multiple JSONL files into one"""
        console.log(f"🔄 Merging files into: {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for input_path in input_paths:
                with open(input_path, 'r', encoding='utf-8') as infile:
                    for line in infile:
                        outfile.write(line)
        
        console.log("[bold green]✅ Files merged successfully![/bold green]")
