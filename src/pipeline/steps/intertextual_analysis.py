from typing import Dict, Any
from openai import OpenAI
from haystack import Document
from rich.console import Console
from .base import PipelineStep
from src.prompts.generator import PromptGenerator
from src.models.schemas import IntertextualAnalysis
from src.config.settings import settings

console = Console()

class IntertextualAnalysisStep(PipelineStep):
    """Step for analyzing intertextual references using LLM"""
    
    def __init__(
        self,
        client: OpenAI,
        prompt_generator: PromptGenerator,
        system_prompt: str
    ):
        self.client = client
        self.prompt_generator = prompt_generator
        self.system_prompt = system_prompt
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query_text: str = input_data["query_text"]
        similar_doc: Document = input_data["similar_document"]
        
        prompt = self.prompt_generator.generate(
            template_name="analysis",
            dalloway_text=query_text,
            odyssey_text=similar_doc.content,
            similarity_score=similar_doc.score
        )
        
        completion = self.client.beta.chat.completions.parse(
            model=settings.llm.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format=IntertextualAnalysis,
            temperature=settings.llm.temperature,
            max_tokens=settings.llm.max_tokens
        )
        
        return {"analysis": completion.choices[0].message.parsed} 