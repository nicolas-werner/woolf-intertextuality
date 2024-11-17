from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, Template
from rich.console import Console

console = Console()

class PromptGenerator:
    """Handles loading and rendering of prompt templates"""
    
    def __init__(self, template_dir: str = "src/prompts/templates"):
        """Initialize the prompt generator with a template directory"""
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def generate(self, template_name: str, **kwargs) -> str:
        """Generate a prompt from a template with variables
        
        Args:
            template_name: Name of the template file (without .j2 extension)
            **kwargs: Variables to pass to the template
            
        Returns:
            Rendered prompt string
            
        Raises:
            TemplateNotFound: If template doesn't exist
            TemplateError: If template rendering fails
        """
        try:
            template = self.env.get_template(f"{template_name}.j2")
            return template.render(**kwargs)
        except Exception as e:
            console.print(f"[red]Error generating prompt from template {template_name}: {str(e)}[/red]")
            raise 