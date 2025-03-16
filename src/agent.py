from typing import Any
from abc import ABC, abstractmethod
from .config import DEFAULT_MODEL

from .interface import UserInterface

class Agent(ABC):
    """Abstract base class for agents."""
    
    def __init__(self, interface: UserInterface, model: str = DEFAULT_MODEL, max_tokens: int = 100):
        if not isinstance(interface, UserInterface):
            raise TypeError("interface must implement UserInterface protocol")
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model must be a non-empty string")
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValueError("max_tokens must be a positive integer")
            
        self.interface = interface
        self.model = model
        self.max_tokens = max_tokens

    @abstractmethod
    def __call__(self, input_text: str) -> str:
        """Process input and return response."""
        raise NotImplementedError






class AgentAssert:
    """Utility class for agent assertions."""
    
class ConcreteAgent(Agent):
    """Concrete agent implementation that handles basic conversational patterns."""
    
    def __init__(self, interface: UserInterface, model: str = DEFAULT_MODEL, max_tokens: int = 100):
        super().__init__(interface, model, max_tokens)
        
    def __call__(self, input_text: str) -> str:
        """Handle input with simple pattern matching."""
        if not isinstance(input_text, str) or not input_text.strip():
            raise ValueError("Input must be a non-empty string")
            
        lower_input = input_text.lower()
        if "hello" in lower_input:
            return "Hello! How can I help you?"
        elif "goodbye" in lower_input:
            return "Goodbye! Have a great day!"
        return "I'm not sure how to respond to that."

    def __repr__(self) -> str:
        return f"ConcreteAgent(model={self.model!r}, max_tokens={self.max_tokens}, interface={self.interface!r})"

