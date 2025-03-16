from typing import Optional
from abc import ABC, abstractmethod
from .config import DEFAULT_MODEL, global_settings
from .interface import UserInterface, ConsoleInterface
from .llm_utils import litellm_completion
from .utils import normalize_model_name


class Agent(ABC):
    """Abstract base class for agents."""
    
    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = 100, interface: Optional[UserInterface] = None):
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model must be a non-empty string")
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValueError("max_tokens must be a positive integer")
            
        self.model = normalize_model_name(model)
        self.max_tokens = max_tokens
        self.net_worth = global_settings['initial_net_worth']
        self.memory = ''
        self.interface = interface or ConsoleInterface()

    @abstractmethod
    def __call__(self, input_text: str) -> str:
        """Process input and return response."""
        raise NotImplementedError
        
    @abstractmethod
    def __repr__(self) -> str:
        """Return string representation of agent."""
        raise NotImplementedError








class AgentAssert(Agent):
    def __call__(self, input_text: str) -> str:
        if not isinstance(input_text, str) or not input_text.strip():
            raise ValueError("Input must be a non-empty string")
            
        if "assert" in input_text.lower():
            return "Assertion validated"
        return "No assertion found"

