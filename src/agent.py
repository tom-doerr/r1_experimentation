from typing import Any, Dict, Protocol
from abc import abstractmethod
from .llm_utils import litellm_completion
from .config import DEFAULT_MODEL, global_settings
from .interface import UserInterface
from .utils import normalize_model_name

class Agent:
    """Main agent class that handles interactions and commands."""
    
    def __init__(self, interface: UserInterface, model: str = DEFAULT_MODEL):
        if not isinstance(interface, UserInterface):
            raise TypeError("interface must implement UserInterface protocol")
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model must be a non-empty string")
            
        self.interface = interface
        self.model = normalize_model_name(model)
        
    def __call__(self, input_text: str) -> str:
        """Handle user input and return response."""
        if not isinstance(input_text, str) or not input_text.strip():
            raise ValueError("input_text must be a non-empty string")
            
        try:
            response = litellm_completion(input_text, self.model, self.max_tokens)
            return response
        except Exception as e:
            self.interface.display_error(f"Error: {str(e)}")
            return "Sorry, I encountered an error."

    def __repr__(self) -> str:
        return f"Agent(model={self.model!r})"

class AgentAssert(Agent):
    """Concrete implementation of Agent for assertion testing."""
    
    def __init__(self, interface: UserInterface, model: str = DEFAULT_MODEL):
        if not isinstance(model, str) or not model.strip():
            raise ValueError("Model must be a non-empty string")
        self.interface = interface
        self.model = normalize_model_name(model)
        
    def __call__(self, input_text: str) -> str:
        """Handle user input and return response."""
        if not isinstance(input_text, str) or not input_text.strip():
            raise ValueError("Input must be a non-empty string")
            
        try:
            response = litellm_completion(input_text, self.model)
            return response
        except Exception as e:
            self.interface.display_error(f"Error: {str(e)}")
            return "Sorry, I encountered an error."
            
    def __repr__(self) -> str:
        return f"AgentAssert(model={self.model!r})"
