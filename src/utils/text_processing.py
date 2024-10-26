import re
from nltk.tokenize import sent_tokenize

def clean_text(text):
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def split_into_chunks(text, method='paragraph', sentences_per_chunk=4):
    if method == 'paragraph':
        return re.split(r'\n\n+', text)
    else:
        sentences = sent_tokenize(text)
        return [' '.join(sentences[i:i+sentences_per_chunk]) for i in range(0, len(sentences), sentences_per_chunk)]