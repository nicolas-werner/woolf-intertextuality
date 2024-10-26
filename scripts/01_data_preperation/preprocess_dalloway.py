import re
from rich.console import Console
from nltk.tokenize import sent_tokenize
import nltk

nltk.download('punkt')

console = Console()

def clean_text(text):
    console.log("🧹 Removing unnecessary newlines")
    text = re.sub(r'\n+', ' ', text)

    console.log("🧼 Removing multiple spaces")
    text = re.sub(r'\s+', ' ', text)

    console.log("✂️ Removing leading/trailing whitespace")
    text = text.strip()

    return text

def preprocess_dalloway(input_file, output_file, chunk_method='paragraph', sentences_per_chunk=4):
    console.log(f"📖 Reading file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Apply original cleaning functions
    text = clean_text(text)

    console.log("📚 Splitting text into paragraphs")
    paragraphs = re.split(r'\n\n+', text)

    processed_chunks = []
    current_chapter = "Chapter 1"  # Assume it starts with Chapter 1

    for i, paragraph in enumerate(paragraphs):
        # Check for chapter changes (you may need to adjust this based on the book's structure)
        if re.match(r'^Chapter \d+', paragraph):
            current_chapter = paragraph.strip()
            continue

        if chunk_method == 'paragraph':
            chunks = [paragraph]
        else:  # sentence-based chunking
            sentences = sent_tokenize(paragraph)
            chunks = [' '.join(sentences[j:j+sentences_per_chunk]) for j in range(0, len(sentences), sentences_per_chunk)]

        for j, chunk in enumerate(chunks):
            # Generate context header
            context = f"Context: Mrs Dalloway by Virginia Woolf, {current_chapter}. "
            context += f"Paragraph {i+1}, " if chunk_method == 'paragraph' else f"Sentences {j*sentences_per_chunk+1}-{(j+1)*sentences_per_chunk}, "
            context += "Themes may include post-war society, memory, and time.\n\n"
            
            processed_chunks.append(context + chunk)

    console.log(f"💾 Writing processed chunks to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(processed_chunks))

    console.log("[bold green]✅ Preprocessing of Mrs. Dalloway complete. Processed file has been created.[/bold green]")

# Process Mrs. Dalloway
input_file = '../../data_src/mrs_dalloway.txt'
output_file = '../../data_src/mrs_dalloway_processed.txt'
preprocess_dalloway(input_file, output_file, chunk_method='sentence', sentences_per_chunk=4)