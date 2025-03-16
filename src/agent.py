from typing import Any, Dict, Protocol
from abc import abstractmethod, ABC
from .llm_utils import litellm_completion
from .config import DEFAULT_MODEL, global_settings
from .interface import UserInterface, ConsoleInterface
from .utils import normalize_model_name

class Agent(ABC):
    """Main agent class that handles interactions and commands."""
    
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

    def __repr__(self) -> str:
        return f"Agent(model={self.model!r}, max_tokens={self.max_tokens})"


class AgentAssert:
    """Utility class for agent assertions and validation."""
    
    @staticmethod
    def validate_agent(agent: Agent) -> None:
        """Validate that an object is a properly configured Agent."""
        if not isinstance(agent, Agent):
            raise TypeError("Must be an Agent instance")
        if not hasattr(agent, '__call__'):
            raise TypeError("Agent must be callable")
        if not hasattr(agent, 'interface'):
            raise AttributeError("Agent must have interface attribute")

