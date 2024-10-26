import re
from rich.console import Console
from rich.progress import track
from nltk.tokenize import sent_tokenize
import nltk

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
        
        # Remove footnotes and clean up text
        book_content = re.sub(r'\[\d+\].*?(?=\n\n|\Z)', '', book_content, flags=re.DOTALL)
        book_content = re.sub(r'\n+', ' ', book_content)
        book_content = re.sub(r'\s+', ' ', book_content)
        book_content = book_content.strip()
        book_content = book_content.replace('"', '"').replace('"', '"')
        book_content = book_content.replace("'", "'")
        book_content = book_content.replace('—', '-')

        # Split into paragraphs or sentences
        if chunk_method == 'paragraph':
            chunks = re.split(r'\n\n+', book_content)
        else:
            sentences = sent_tokenize(book_content)
            chunks = [' '.join(sentences[i:i+sentences_per_chunk]) for i in range(0, len(sentences), sentences_per_chunk)]

        for j, chunk in enumerate(chunks):
            # Generate context header
            context = f"Context: The Odyssey by Homer, {book_title}. "
            context += f"Paragraph {j+1}, " if chunk_method == 'paragraph' else f"Sentences {j*sentences_per_chunk+1}-{(j+1)*sentences_per_chunk}, "
            context += "Themes may include heroism, homecoming, and divine intervention.\n\n"
            
            processed_chunks.append(context + chunk)

    console.log(f"💾 Writing processed chunks to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(processed_chunks))

    console.log("[bold green]✅ Preprocessing of Odyssey complete. Processed file has been created.[/bold green]")

# Process Odyssey (Butcher translation)
input_file = '../../data_src/odyssey_butcher.txt'
output_file = '../../data_src/odyssey_butcher_processed.txt'
preprocess_odyssey(input_file, output_file, chunk_method='sentence', sentences_per_chunk=4)