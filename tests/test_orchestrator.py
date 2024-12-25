from src.pipeline.orchestrator import PipelineOrchestrator


def test_orchestrator_execution_flows(token_counter, sample_documents):
    orchestrator = PipelineOrchestrator(token_counter=token_counter)

    # Test indexing flow
    result = orchestrator.execute({"documents": sample_documents})
    assert result is not None

    # Test similarity search flow
    query_text = sample_documents[0].content
    result = orchestrator.execute({"query_text": query_text})
    assert "similar_documents" in result

    # Test analysis flow
    document = sample_documents[1]
    document.score = 0.8
    document.meta["similarity_type"] = "similar"
    result = orchestrator.execute({"query_text": query_text, "document": document})
    assert "analysis" in result
