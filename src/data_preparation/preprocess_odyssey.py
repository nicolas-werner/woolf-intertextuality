import re
from rich.console import Console
from rich.progress import track
from nltk.tokenize import sent_tokenize
import nltk
import os
from src.utils.text_processing import clean_text, split_into_chunks

nltk.download('punkt')

console = Console()

def preprocess_odyssey(input_file, output_file, chunk_method='paragraph', sentences_per_chunk=4):
    console.log(f"📖 Reading file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    console.log("📚 Splitting text into books")
    books = re.split(r'(BOOK [IVXLCDM]+\.)', text)[1:]  # [1:] to skip the initial empty string
    processed_chunks = []

    for i in track(range(0, len(books), 2), description="📚 Processing books"):
        book_title = books[i].strip()
        book_content = books[i+1]

        console.log(f"🔍 Processing {book_title}")
        
        book_content = clean_text(book_content)
        chunks = split_into_chunks(book_content, method=chunk_method, sentences_per_chunk=sentences_per_chunk)

        for j, chunk in enumerate(chunks):
            # Generate context header
            context = f"Context: The Odyssey by Homer, {book_title}. "
            context += f"Chunk {j+1}, "
            context += "Themes may include heroism, homecoming, and divine intervention.\n\n"
            
            processed_chunks.append(context + chunk)

    console.log(f"💾 Writing processed chunks to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(processed_chunks))

    console.log("[bold green]✅ Preprocessing of Odyssey complete. Processed file has been created.[/bold green]")

def main():
    input_file = os.path.join('data', 'raw', 'odyssey_butcher.txt')
    output_file = os.path.join('data', 'processed', 'odyssey_butcher_processed.txt')
    preprocess_odyssey(input_file, output_file, chunk_method='sentence', sentences_per_chunk=4)

if __name__ == "__main__":
    main()