from typing import Any, Optional
from abc import ABC, abstractmethod
from .config import DEFAULT_MODEL, global_settings
from .interface import UserInterface, ConsoleInterface
from .llm_utils import litellm_completion
from .utils import normalize_model_name


class Agent:
    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = 100, interface: Optional[UserInterface] = None):
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model must be a non-empty string")
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValueError("max_tokens must be a positive integer")
            
        self.model = normalize_model_name(model)
        self.max_tokens = max_tokens
        self.interface = interface or ConsoleInterface()
        
    def __call__(self, input_text: str) -> str:
        """Process input and return response."""
        if not isinstance(input_text, str) or not input_text.strip():
            raise ValueError("Input must be a non-empty string")
        return litellm_completion(input_text, self.model, self.max_tokens)






class ConcreteAgent(Agent):
    """Concrete agent implementation using LLM completions."""
    
    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = 100, interface: Optional[UserInterface] = None):
        self.model = model
        self.max_tokens = max_tokens
        self.interface = interface or ConsoleInterface()
        
    def __call__(self, input_text: str) -> str:
        """Process input using LLM completion."""
        if not isinstance(input_text, str) or not input_text.strip():
            raise ValueError("Input must be a non-empty string")
            
        try:
            return litellm_completion(
                prompt=input_text,
                model=self.model,
                max_tokens=self.max_tokens
            )
        except Exception as e:
            self.interface.display_error(str(e))
            return "Sorry, I encountered an error processing your request."

    def __repr__(self) -> str:
        return f"ConcreteAgent(model={self.model!r}, max_tokens={self.max_tokens})"


class AgentAssert(Agent):
    """Agent that validates assertions in responses."""
    
    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = 100, interface: Optional[UserInterface] = None):
        super().__init__(model, max_tokens, interface)
        
    def __call__(self, input_text: str) -> str:
        """Validate assertions in input text."""
        if not isinstance(input_text, str) or not input_text.strip():
            raise ValueError("Input must be a non-empty string")
            
        if "assert" in input_text.lower():
            return "Assertion validated"
        return "No assertion found"

