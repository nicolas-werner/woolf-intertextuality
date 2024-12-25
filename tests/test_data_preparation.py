from haystack import Document
from src.data_preparation.preprocessing import TextPreprocessor


def test_text_preprocessing():
    preprocessor = TextPreprocessor()
    text = "This is a test. This is another test."
    doc = Document(content=text)

    # Test cleaning
    cleaned_docs = preprocessor.cleaner.run(documents=[doc])["documents"]
    assert len(cleaned_docs) > 0
    assert all(isinstance(doc, Document) for doc in cleaned_docs)

    # Test splitting
    split_docs = preprocessor.splitter.run(documents=cleaned_docs)["documents"]
    assert len(split_docs) > 0
    assert all(isinstance(doc, Document) for doc in split_docs)


def test_dalloway_preprocessing(tmp_path):
    preprocessor = TextPreprocessor()

    # Create a test file
    test_file = tmp_path / "test_dalloway.txt"
    test_file.write_text("Mrs Dalloway said she would buy the flowers herself.")

    # Test processing
    chunks = preprocessor.get_dalloway_queries(str(test_file))
    assert len(chunks) > 0
    assert all(isinstance(doc, Document) for doc in chunks)
    assert all("source" in doc.meta for doc in chunks)
    assert all(doc.meta["source"] == "Mrs Dalloway" for doc in chunks)


def test_odyssey_preprocessing(tmp_path):
    preprocessor = TextPreprocessor()

    # Create a test file
    test_file = tmp_path / "test_odyssey.txt"
    test_file.write_text("BOOK I.\nTell me, O Muse, of the man of many devices.")

    # Test processing
    chunks = preprocessor.process_odyssey(str(test_file))
    assert len(chunks) > 0
    assert all(isinstance(doc, Document) for doc in chunks)
    assert all("chapter" in doc.meta for doc in chunks)
    assert all("book_number" in doc.meta for doc in chunks)
