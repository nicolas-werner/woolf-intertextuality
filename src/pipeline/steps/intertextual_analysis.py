from typing import Dict, Any
from openai import OpenAI
from haystack import Document
from rich.console import Console
from .base import PipelineStep
from src.prompts.generator import PromptGenerator
from src.models.schemas import Analysis
from src.config.settings import settings
from src.utils.token_counter import TokenCounter

console = Console()


class IntertextualAnalysisStep(PipelineStep):
    """Step for analyzing intertextual references using LLM"""

    def __init__(
        self,
        client: OpenAI,
        prompt_generator: PromptGenerator,
        system_prompt: str,
        token_counter: TokenCounter,
    ):
        self.client = client
        self.prompt_generator = prompt_generator
        self.system_prompt = system_prompt
        self.token_counter = token_counter

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query_text: str = input_data["query_text"]
        doc: Document = input_data["document"]

        prompt = self.prompt_generator.generate(
            template_name="analysis",
            dalloway_text=query_text,
            odyssey_text=doc.content,
            similarity_score=doc.score,
            similarity_type=doc.meta["similarity_type"],
        )

        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]

        try:
            console.log("[cyan]Sending request to OpenAI...[/cyan]")
            completion = self.client.beta.chat.completions.parse(
                model=settings.llm.model,
                messages=messages,
                response_format=Analysis,
                temperature=settings.llm.temperature,
                max_tokens=settings.llm.max_tokens,
            )

            self.token_counter.track_completion(
                messages=messages,
                completion_tokens=completion.usage.completion_tokens if hasattr(completion, 'usage') else None,
            )

            console.log("[green]Analysis result created successfully[/green]")
            return completion.choices[0].message.parsed

        except Exception as e:
            console.print(f"[red]Error in LLM analysis: {str(e)}[/red]")
            console.print(f"[red]Input data: {input_data}[/red]")
            raise
