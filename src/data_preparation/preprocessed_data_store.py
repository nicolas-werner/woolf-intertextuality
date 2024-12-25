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

    def save_chunks(
        self, documents: Union[List[Document], List[Dict]], output_path: str
    ) -> None:
        """Save preprocessed chunks with their metadata and embeddings"""
        console.log(f"💾 Saving chunks to: {output_path}")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        total_with_embeddings = 0
        with open(output_path, "w", encoding="utf-8", errors="replace") as f:
            for doc in documents:
                # Handle both Document objects and dictionaries
                if isinstance(doc, Document):
                    doc_dict = {
                        "content": doc.content,
                        "meta": doc.meta,
                    }
                    # Check for embedding
                    if hasattr(doc, "embedding") and doc.embedding is not None:
                        if isinstance(doc.embedding, np.ndarray):
                            doc_dict["embedding"] = doc.embedding.tolist()
                            total_with_embeddings += 1
                        else:
                            doc_dict["embedding"] = doc.embedding
                            total_with_embeddings += 1
                        console.log(
                            f"[green]Saving document with embedding of size {len(doc.embedding)}[/green]"
                        )
                else:
                    doc_dict = doc
                    if "embedding" in doc_dict:
                        total_with_embeddings += 1

                json_str = json.dumps(doc_dict, ensure_ascii=False)
                f.write(json_str + "\n")

        console.log(
            f"[bold green]✅ Saved {len(documents)} chunks ({total_with_embeddings} with embeddings)![/bold green]"
        )

    def load_chunks(self, input_path: str) -> List[Document]:
        """Load preprocessed chunks with embeddings"""
        console.log(f"📖 Loading chunks from: {input_path}")

        documents = []
        total_with_embeddings = 0

        with open(input_path, "r", encoding="utf-8", errors="replace") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    chunk = json.loads(line)
                    content = chunk.get("content", chunk.get("text", ""))
                    meta = chunk.get("meta", {})

                    # Convert embedding back to numpy array if it exists
                    embedding = None
                    if "embedding" in chunk:
                        embedding = np.array(chunk["embedding"])
                        total_with_embeddings += 1
                        # console.log(f"[green]Found cached embedding of size {len(embedding)} in chunk {line_num}[/green]")

                    documents.append(
                        Document(content=content, meta=meta, embedding=embedding)
                    )
                except Exception as e:
                    console.log(f"[red]Error loading chunk {line_num}: {str(e)}[/red]")

        console.log(
            f"[bold green]✅ Loaded {len(documents)} chunks ({total_with_embeddings} with embeddings)![/bold green]"
        )

        # Validate embeddings
        # for i, doc in enumerate(documents):
        #     if doc.embedding is not None:
        #         console.log(f"[green]Chunk {i+1} has embedding of size {len(doc.embedding)}[/green]")
        #     else:
        #         console.log(f"[yellow]Warning: Chunk {i+1} has no embedding[/yellow]")

        return documents

    def merge_files(self, input_paths: List[str], output_path: str) -> None:
        """Merge multiple JSONL files into one"""
        console.log(f"🔄 Merging files into: {output_path}")

        with open(output_path, "w", encoding="utf-8") as outfile:
            for input_path in input_paths:
                with open(input_path, "r", encoding="utf-8") as infile:
                    for line in infile:
                        outfile.write(line)

        console.log("[bold green]✅ Files merged successfully![/bold green]")
