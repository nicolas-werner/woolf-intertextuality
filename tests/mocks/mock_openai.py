from typing import List, Dict
import json


class MockOpenAIResponse:
    def __init__(self, content: str, usage: Dict[str, int]):
        self.choices = [
            type("Choice", (), {"message": type("Message", (), {"content": content})})()
        ]
        self.usage = type("Usage", (), usage)()


class MockOpenAI:
    """Mock OpenAI client for testing"""

    def __init__(self, api_key: str = "fake-key"):
        self.chat = type("Chat", (), {"completions": self})()

    def create(
        self, model: str, messages: List[Dict[str, str]], **kwargs
    ) -> MockOpenAIResponse:
        """Mock chat completion"""
        mock_analysis = {
            "introduction": "Mock introduction to the analysis",
            "process": {
                "initial_observation": "Mock initial observation",
                "steps": [
                    {
                        "step_description": "Mock analysis step",
                        "evidence": "Mock evidence",
                        "theoretical_reference": "Mock theoretical framework",
                        "contrasting_evidence": "Mock contrasting evidence",
                    }
                ],
                "synthesis_with_implications": "Mock synthesis",
                "counterpoints": ["Mock counterpoint 1", "Mock counterpoint 2"],
            },
            "intersections": {
                "confidence": "high",
                "intersection_details": [
                    {
                        "specific_elements": ["Mock element 1", "Mock element 2"],
                        "relationship_types": ["intertextual", "dialogic"],
                        "transformation_types": ["thematic", "cultural"],
                        "meaning_analysis": "Mock meaning analysis",
                        "contextual_significance": "Mock contextual significance",
                        "relationship_evaluation": "Mock relationship evaluation",
                    }
                ],
                "evidence_passages": ["Mock evidence passage 1", "Mock evidence passage 2"],
                "novelty": "Mock novel insight",
            },
            "critique": "Mock critique",
            "recommendations": "Mock recommendations for future research",
        }

        # Ensure clean JSON serialization
        return MockOpenAIResponse(
            content=json.dumps(mock_analysis, ensure_ascii=False),
            usage={"completion_tokens": 100},
        )

    def embed_query(self, text: str) -> List[float]:
        """Mock embedding generation"""
        return [0.1] * 1536  # OpenAI's embedding dimension

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Mock document embedding"""
        return [[0.1] * 1536 for _ in texts]
