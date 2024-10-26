import re
from rich.console import Console
from nltk.tokenize import sent_tokenize
import nltk
import os
from src.utils.text_processing import clean_text, split_into_chunks

nltk.download('punkt')

console = Console()

def preprocess_dalloway(input_file, output_file, chunk_method='paragraph', sentences_per_chunk=4):
    console.log(f"📖 Reading file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    text = clean_text(text)

    console.log("📚 Splitting text into chunks")
    chunks = split_into_chunks(text, method=chunk_method, sentences_per_chunk=sentences_per_chunk)

    processed_chunks = []
    current_chapter = "Chapter 1"  # Assume it starts with Chapter 1

    for i, chunk in enumerate(chunks):
        # Check for chapter changes (you may need to adjust this based on the book's structure)
        if re.match(r'^Chapter \d+', chunk):
            current_chapter = chunk.strip()
            continue

        # Generate context header
        context = f"Context: Mrs Dalloway by Virginia Woolf, {current_chapter}. "
        context += f"Chunk {i+1}, "
        context += "Themes may include post-war society, memory, and time.\n\n"
        
        processed_chunks.append(context + chunk)

    console.log(f"💾 Writing processed chunks to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(processed_chunks))

    console.log("[bold green]✅ Preprocessing of Mrs. Dalloway complete. Processed file has been created.[/bold green]")

def main():
    input_file = os.path.join('data', 'raw', 'mrs_dalloway.txt')
    output_file = os.path.join('data', 'processed', 'mrs_dalloway_processed.txt')
    preprocess_dalloway(input_file, output_file, chunk_method='sentence', sentences_per_chunk=4)

if __name__ == "__main__":
    main()