import pytest
from haystack import Document
from src.utils.token_counter import TokenCounter
from src.pipeline.pipeline_facade import PipelineFacade
from src.config.settings import settings
from tests.mocks.mock_openai import MockOpenAI


@pytest.fixture
def mock_openai():
    return MockOpenAI()


@pytest.fixture
def token_counter():
    return TokenCounter()


@pytest.fixture
def pipeline(token_counter, mock_openai, monkeypatch):
    """Create pipeline with mocked OpenAI client"""

    # Patch the OpenAI client creation in the orchestrator
    def mock_create_client(*args, **kwargs):
        return mock_openai

    monkeypatch.setattr("src.pipeline.orchestrator.OpenAI", mock_create_client)
    return PipelineFacade(token_counter=token_counter)


@pytest.fixture
def sample_documents():
    return [
        Document(
            content="Clarissa Dalloway said she would buy the flowers herself.",
            meta={"chapter": 1},
        ),
        Document(
            content="Tell me, O Muse, of the man of many devices.", meta={"chapter": 1}
        ),
    ]


@pytest.fixture
def mock_embeddings():
    return [0.1] * settings.embeddings.dimension
