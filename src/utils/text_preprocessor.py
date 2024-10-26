import re
from pathlib import Path
from typing import List, Dict
from rich.console import Console
from rich.progress import track
from haystack.nodes import PreProcessor
from src.config.settings import settings

console = Console()

class TextPreprocessor:
    def __init__(self):
        # Initialize Haystack preprocessor for text splitting
        self.haystack_preprocessor = PreProcessor(
            clean_empty_lines=True,
            clean_whitespace=True,
            clean_header_footer=False,
            split_by=settings.preprocessing.strategy,
            split_length=settings.preprocessing.chunk_size,
            split_overlap=settings.preprocessing.chunk_overlap,
            split_respect_sentence_boundary=True
        )
        
        self.include_context_header = settings.preprocessing.include_context_header

    def _clean_text(self, text: str) -> str:
        """Initial cleaning of raw text files"""
        text = re.sub(r'\[\d+\].*?(?=\n\n|\Z)', '', text, flags=re.DOTALL)  # Remove footnotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace("'", "'")
        text = text.replace('—', '-')
        return text.strip()

    def get_dalloway_queries(self, input_file: str) -> List[Dict]:
        """Process Mrs Dalloway text and return chunks for querying"""
        console.log(f"📖 Reading Mrs Dalloway for queries: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # Initial cleaning
        text = self._clean_text(text)
        
        # Use Haystack's preprocessor to split text
        docs = self.haystack_preprocessor.process([{"content": text}])
        
        # Convert to query chunks with metadata
        query_chunks = []
        for i, doc in enumerate(docs, 1):
            query_chunks.append({
                "content": doc.content,
                "metadata": {
                    "source": "Mrs Dalloway",
                    "chunk_number": i
                }
            })
        return query_chunks

    def process_odyssey(self, input_file: str) -> List[Dict]:
        """Process The Odyssey text and return chunks with metadata"""
        console.log(f"📖 Reading The Odyssey: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()

        books = re.split(r'(BOOK [IVXLCDM]+\.)', text)[1:]
        processed_chunks = []

        for i in track(range(0, len(books), 2), description="📚 Processing books"):
            book_title = books[i].strip()
            book_content = books[i+1]
            book_num = i // 2 + 1

            # Initial cleaning
            book_content = self._clean_text(book_content)
            
            # Use Haystack's preprocessor to split text
            docs = self.haystack_preprocessor.process([{"content": book_content}])

            for chunk_num, doc in enumerate(docs, 1):
                if self.include_context_header:
                    content = f"Context: The Odyssey, {book_title}. Chunk {chunk_num}\n\n{doc.content}"
                else:
                    content = doc.content

                processed_chunks.append({
                    "content": content,
                    "metadata": {
                        "chapter": book_title,
                        "book_number": book_num,
                        "chunk_number": chunk_num
                    }
                })

        return processed_chunks
