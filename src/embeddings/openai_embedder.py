from haystack.nodes.retriever import EmbeddingRetriever
from openai import OpenAI
from typing import List, Union, Any
from src.config.settings import settings

class OpenAIEmbeddingRetriever(EmbeddingRetriever):
    def __init__(self, document_store: Any) -> None:
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.document_store = document_store
        self.model_name = settings.embeddings.model_name
        
    def embed(self, text: Union[str, List[str]]) -> List[float]:
        """Get embeddings from OpenAI API"""
        if isinstance(text, list):
            return self.embed_batch(text)
            
        response = self.client.embeddings.create(
            model=self.model_name,
            input=text
        )
        return response.data[0].embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for a batch of texts"""
        response = self.client.embeddings.create(
            model=self.model_name,
            input=texts
        )
        return [data.embedding for data in response.data]
