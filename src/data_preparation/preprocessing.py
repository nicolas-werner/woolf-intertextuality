import re
from pathlib import Path
from typing import List, Dict
from rich.console import Console
from rich.progress import track
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter, TextCleaner
from haystack import Document
from src.config.settings import settings

console = Console()

class TextPreprocessor:
    """Handles text preprocessing and chunking for both texts"""
    
    def __init__(self):
        # Initialize text cleaner for initial raw text cleaning
        self.text_cleaner = TextCleaner(
            remove_regexps=[r'\[\d+\].*?(?=\n\n|\Z)'],  # Remove footnotes
            convert_to_lowercase=False,
            remove_punctuation=False,
            remove_numbers=False
        )
        
        # Initialize document cleaner for structural cleaning
        self.cleaner = DocumentCleaner(
            remove_empty_lines=True,
            remove_extra_whitespaces=True,
            remove_repeated_substrings=False,
            unicode_normalization="NFKC"  # Normalize unicode characters
        )
        
        self.splitter = DocumentSplitter(
            split_by=settings.preprocessing.strategy,
            split_length=settings.preprocessing.chunk_size,
            split_overlap=settings.preprocessing.chunk_overlap,
            split_threshold=0
        )
        
        self.include_context_header = settings.preprocessing.include_context_header

    def _clean_text(self, text: str) -> str:
        """Initial cleaning of raw text using Haystack's TextCleaner"""
        cleaned_text = self.text_cleaner.run(texts=[text])["texts"][0]
        return cleaned_text

    def get_dalloway_queries(self, input_file: str) -> List[Document]:
        """Process Mrs Dalloway text and return chunks for querying"""
        console.log(f"📖 Reading Mrs Dalloway for queries: {input_file}")
        with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()

        # Initial cleaning
        text = self._clean_text(text)
        
        # Create initial document
        doc = Document(content=text)
        
        # Clean and split the document
        cleaned_docs = self.cleaner.run(documents=[doc])["documents"]
        split_docs = self.splitter.run(documents=cleaned_docs)["documents"]
        
        # Add metadata to documents
        for i, doc in enumerate(split_docs, 1):
            doc.meta = {
                "source": "Mrs Dalloway",
                "chunk_number": i
            }
        
        return split_docs

    def process_odyssey(self, input_file: str) -> List[Document]:
        """Process The Odyssey text and return chunks with metadata"""
        console.log(f"📖 Reading The Odyssey: {input_file}")
        with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()

        books = re.split(r'(BOOK [IVXLCDM]+\.)', text)[1:]
        processed_chunks = []

        for i in track(range(0, len(books), 2), description="📚 Processing books"):
            book_title = books[i].strip()
            book_content = books[i+1]
            book_num = i // 2 + 1

            # Initial cleaning
            book_content = self._clean_text(book_content)
            
            # Create initial document
            doc = Document(content=book_content)
            
            # Clean and split the document
            cleaned_docs = self.cleaner.run(documents=[doc])["documents"]
            split_docs = self.splitter.run(documents=cleaned_docs)["documents"]

            for chunk_num, doc in enumerate(split_docs, 1):
                if self.include_context_header:
                    doc.content = doc.content
                
                doc.meta = {
                    "chapter": book_title,
                    "book_number": book_num,
                    "chunk_number": chunk_num
                }
                processed_chunks.append(doc)

        return processed_chunks 