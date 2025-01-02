from typing import Dict, List, Optional
import tiktoken
from rich.console import Console

console = Console()


class TokenCounter:
    """Tracks token usage and estimates costs for OpenAI API calls"""

    PRICING = {
        "gpt-4o": {
            "input": 0.0025,  # $2.50 per 1M tokens = $0.0025 per 1k
            "output": 0.01,  # $10.00 per 1M tokens = $0.01 per 1k
            "cached_input": 0.00125,  # $1.25 per 1M tokens = $0.00125 per 1k
        },
        "text-embedding-3-small": {"input": 0.00002, "output": 0.00002},
    }

    def __init__(self):
        self.usage = {
            "embedding": {"tokens": 0, "cost": 0.0},
            "completion": {
                "input_tokens": 0,
                "cached_input_tokens": 0,
                "output_tokens": 0,
                "cost": 0.0,
            },
        }
        self.encoding = tiktoken.encoding_for_model("gpt-4o")

    def count_tokens(self, text: str) -> int:
        """Count tokens for a given text"""
        return len(self.encoding.encode(text))

    def count_message_tokens(self, messages: List[Dict[str, str]]) -> int:
        """Count tokens in a message list for chat completion"""
        num_tokens = 0
        for message in messages:
            # Every message follows <im_start>{role/name}\n{content}<im_end>\n
            num_tokens += 4
            for key, value in message.items():
                num_tokens += self.count_tokens(value)
        num_tokens += 2  # Every reply is primed with <im_start>assistant
        return num_tokens

    def track_embedding(self, texts: List[str]):
        """Track token usage for embeddings"""
        total_tokens = sum(self.count_tokens(text) for text in texts)
        cost = (total_tokens / 1000) * self.PRICING["text-embedding-3-small"]["input"]

        self.usage["embedding"]["tokens"] += total_tokens
        self.usage["embedding"]["cost"] += cost

    def track_completion(self, messages: List[Dict[str, str]], completion_tokens: Optional[int] = None):
        """Track token usage for a completion."""
        prompt_tokens = self.count_message_tokens(messages)
        
        if completion_tokens is not None:
            self.usage["completion"]["output_tokens"] += completion_tokens
            output_cost = (completion_tokens / 1000) * self.PRICING["gpt-4o"]["output"]
            self.usage["completion"]["cost"] += output_cost

        self.usage["completion"]["input_tokens"] += prompt_tokens
        input_cost = (prompt_tokens / 1000) * self.PRICING["gpt-4o"]["input"]
        self.usage["completion"]["cost"] += input_cost

    def print_usage_report(self):
        """Print token usage and cost report"""
        console.print("\n[bold]Token Usage and Cost Report[/bold]")

        console.print("\n[cyan]Embeddings:[/cyan]")
        console.print(f"Tokens: {self.usage['embedding']['tokens']:,}")
        console.print(f"Cost: ${self.usage['embedding']['cost']:.4f}")

        console.print("\n[cyan]Completions:[/cyan]")
        console.print(
            f"Standard Input tokens: {self.usage['completion']['input_tokens']:,}"
        )
        console.print(
            f"Cached Input tokens: {self.usage['completion']['cached_input_tokens']:,}"
        )
        console.print(f"Output tokens: {self.usage['completion']['output_tokens']:,}")
        console.print(f"Cost: ${self.usage['completion']['cost']:.4f}")

        total_cost = self.usage["embedding"]["cost"] + self.usage["completion"]["cost"]
        console.print(f"\n[green]Total Cost: ${total_cost:.4f}[/green]")
