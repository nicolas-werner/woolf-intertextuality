def test_document_indexing_step(pipeline, sample_documents):
    # Test document indexing
    result = pipeline.index_documents(sample_documents)
    assert result is None  # Should return None on success


def test_similarity_search_step(pipeline, sample_documents):
    # First index the documents
    pipeline.index_documents(sample_documents)

    # Test finding similar passages
    query_text = sample_documents[0].content
    results = pipeline.find_similar_passages(query_text)

    assert len(results) > 0
    assert all(hasattr(doc, "score") for doc in results)
    assert all(
        doc.meta.get("similarity_type") in ["similar", "dissimilar"] for doc in results
    )


def test_analysis_step(pipeline, sample_documents, mock_openai, monkeypatch):
    # Add mock_openai and monkeypatch to parameters
    # Patch OpenAI
    def mock_create_client(*args, **kwargs):
        return mock_openai

    monkeypatch.setattr("openai.OpenAI", mock_create_client)

    # Test analyzing a specific pair
    query_text = sample_documents[0].content
    document = sample_documents[1]
    document.score = 0.8
    document.meta["similarity_type"] = "similar"

    analysis = pipeline.analyze_similarity(query_text, document)

    # Test thought process
    assert analysis.thought_process.initial_observation
    assert len(analysis.thought_process.analytical_steps) > 0
    assert analysis.thought_process.synthesis
    assert analysis.thought_process.theoretical_grounding
    assert "kristeva" in analysis.thought_process.theoretical_grounding

    # Test structured analysis
    assert isinstance(analysis.structured_analysis.is_meaningful, bool)
    assert analysis.structured_analysis.confidence in ["low", "medium", "high"]
    assert len(analysis.structured_analysis.intersections) > 0
    
    # Test new fields
    intersection = analysis.structured_analysis.intersections[0]
    assert intersection.feminist_reimagining is not None
    assert intersection.integration_technique is not None
