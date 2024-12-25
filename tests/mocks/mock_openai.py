from typing import List, Dict, Any
import json

class MockOpenAIResponse:
    def __init__(self, content: str, usage: Dict[str, int]):
        self.choices = [
            type('Choice', (), {
                'message': type('Message', (), {'content': content})
            })()
        ]
        self.usage = type('Usage', (), usage)()

class MockOpenAI:
    """Mock OpenAI client for testing"""
    def __init__(self, api_key: str = "fake-key"):
        self.chat = type('Chat', (), {
            'completions': self
        })()
    
    def create(self, model: str, messages: List[Dict[str, str]], **kwargs) -> MockOpenAIResponse:
        """Mock chat completion"""
        mock_analysis = {
            "thought_process": {
                "initial_observation": "Mock observation about the passages",
                "analytical_steps": [
                    {
                        "step_description": "Mock analysis step",
                        "evidence": "Mock textual evidence"
                    }
                ],
                "counter_arguments": ["Mock counter argument"],
                "synthesis": "Mock synthesis of the analysis"
            },
            "structured_analysis": {
                "is_meaningful": True,
                "confidence": "high",
                "intersections": [
                    {
                        "surface_elements": ["Mock element"],
                        "transformation": "thematic",
                        "dialogic_aspects": "direct",
                        "meaning_transformation": "Mock meaning transformation description"
                    }
                ],
                "supporting_evidence": ["Mock evidence for the analysis"]
            },
            "critique": "Mock critique of the analysis"
        }
        
        # Ensure clean JSON serialization
        return MockOpenAIResponse(
            content=json.dumps(mock_analysis, ensure_ascii=False),
            usage={"completion_tokens": 100}
        )

    def embed_query(self, text: str) -> List[float]:
        """Mock embedding generation"""
        return [0.1] * 1536  # OpenAI's embedding dimension

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Mock document embedding"""
        return [[0.1] * 1536 for _ in texts] 