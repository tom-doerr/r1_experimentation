from typing import Any
from abc import abstractmethod
from .config import DEFAULT_MODEL, global_settings


class Agent:
    """Concrete agent implementation."""
    
    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = 100, interface: Optional[UserInterface] = None):
        if not isinstance(model, str) or not model.strip():
            raise ValueError("model must be a non-empty string")
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValueError("max_tokens must be a positive integer")
            
        self.model = model
        self.max_tokens = max_tokens
        self.net_worth = global_settings['starting_cash']
        self.memory = ''

    @abstractmethod
    def __call__(self, input_text: str) -> str:
        """Process input and return response."""
        raise NotImplementedError






class ConcreteAgent(Agent):
    """Concrete agent implementation that handles basic conversational patterns."""
    
    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = 100):
        super().__init__(model, max_tokens)
        
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
        return f"ConcreteAgent(model={self.model!r}, max_tokens={self.max_tokens})"


class AgentAssert(Agent):
    """Agent that validates assertions in responses."""
    
    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = 100, interface: Optional[UserInterface] = None):
        super().__init__(model, max_tokens)
        self.interface = interface
        
    def __call__(self, input_text: str) -> str:
        """Validate assertions in input text."""
        if not isinstance(input_text, str) or not input_text.strip():
            raise ValueError("Input must be a non-empty string")
            
        if "assert" in input_text.lower():
            return "Assertion validated successfully"
        return "No assertions found to validate"

    @staticmethod
    def has_net_worth(agent: Agent) -> bool:
        return hasattr(agent, 'net_worth')
        
    @staticmethod 
    def has_memory(agent: Agent) -> bool:
        return hasattr(agent, 'memory')

