from typing import Any, Dict, Protocol
from abc import abstractmethod
from abc import abstractmethod
from abc import abstractmethod
from .llm_utils import litellm_completion
from .config import DEFAULT_MODEL

class Agent(Protocol):
    """Protocol defining the interface for an agent."""
    
    @abstractmethod
    def __call__(self, input: str) -> str:
        """Process input and return response."""
        raise NotImplementedError("Subclasses must implement __call__")
        
    @abstractmethod
    def __repr__(self) -> str:
        """Return string representation of agent."""
        raise NotImplementedError("Subclasses must implement __repr__")

class AgentAssert:
    """Concrete implementation of Agent for assertion testing."""
    
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        
    def __call__(self, input: str) -> str:
        """Process input using LLM and return response."""
        try:
            return litellm_completion(input, self.model)
        except Exception as e:
            return f"Error: {str(e)}"
            
    def __repr__(self) -> str:
        return f"AgentAssert(model={self.model})"
