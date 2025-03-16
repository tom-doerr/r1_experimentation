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
    
