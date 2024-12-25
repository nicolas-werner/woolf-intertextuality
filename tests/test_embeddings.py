import pytest
from src.embeddings.openai_embedder import OpenAIEmbedder
from haystack import Document
from src.vector_store.qdrant_store import QdrantManager

def test_embedding_generation(sample_documents, mock_openai, monkeypatch):
    # Patch the OpenAI client creation
    def mock_create_client(*args, **kwargs):
        return mock_openai
    monkeypatch.setattr("openai.OpenAI", mock_create_client)
    
    embedder = OpenAIEmbedder()
    
    # Test single query embedding
    query_embedding = embedder.embed_query("test query")
    assert len(query_embedding) == 1536  # OpenAI's embedding dimension
    
    # Test document embedding
    embedded_docs = embedder.embed_documents(sample_documents)
    assert len(embedded_docs) == len(sample_documents)
    assert all(hasattr(doc, 'embedding') for doc in embedded_docs)
    assert all(len(doc.embedding) == 1536 for doc in embedded_docs)

def test_document_store_integration(mock_openai, monkeypatch):
    # Create a QdrantManager instance first
    vector_store = QdrantManager(embedding_dim=1536)
    
    # Patch the OpenAI client creation
    def mock_create_client(*args, **kwargs):
        return mock_openai
    monkeypatch.setattr("openai.OpenAI", mock_create_client)
    
    # Pass document_store to embedder
    embedder = OpenAIEmbedder(document_store=vector_store.document_store)
    assert embedder.document_store is not None 