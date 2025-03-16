from typing import Any, Dict, Protocol
from abc import abstractmethod, ABC
from .llm_utils import litellm_completion
from .config import DEFAULT_MODEL, global_settings
from .interface import UserInterface, ConsoleInterface
from .utils import normalize_model_name

class Agent(ABC):
    """Main agent class that handles interactions and commands."""
    
    @abstractmethod
    def __init__(self, interface: UserInterface = None, model: str = DEFAULT_MODEL, max_tokens: int = 100):
        if interface is None:
            interface = ConsoleInterface()
        if not isinstance(interface, UserInterface):
            raise TypeError("interface must implement UserInterface protocol")
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model must be a non-empty string")
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValueError("max_tokens must be a positive integer")
            
        self.interface = interface
        self.model = normalize_model_name(model)
        self.max_tokens = max_tokens
        
    @abstractmethod
    def __call__(self, input_text: str) -> str:
        """Handle user input and return response."""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

class AgentAssert(Agent):
    """Concrete implementation of Agent for assertion testing."""
    
    def __init__(self, interface: UserInterface, model: str = DEFAULT_MODEL):
        if not isinstance(model, str) or not model.strip():
            raise ValueError("Model must be a non-empty string")
        super().__init__(interface, model)
        
    def __call__(self, input_text: str) -> str:
        """Process input using LLM and return response."""
        if not isinstance(input_text, str) or not input_text.strip():
            raise ValueError("Input must be a non-empty string")
            
        try:
            return litellm_completion(input_text, self.model)
        except Exception as e:
            return f"Error: {str(e)}"
            
    def __repr__(self) -> str:
        return f"AgentAssert(model={self.model!r})"
        
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
