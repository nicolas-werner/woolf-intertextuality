from abc import ABC, abstractmethod
from typing import Any, Dict


class PipelineStep(ABC):
    """Abstract base class for pipeline steps"""

    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the pipeline step

        Args:
            input_data: Dictionary containing input data from previous steps

        Returns:
            Dictionary containing output data to pass to next step
        """
        pass
