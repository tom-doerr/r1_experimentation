from typing import Any, Dict, Protocol
from abc import abstractmethod
from .llm_utils import litellm_completion
from .config import DEFAULT_MODEL
from .interface import UserInterface
from .interface import UserInterface

class Agent:
    """Main agent class that handles interactions and commands."""
    
    def __init__(self, interface: UserInterface, model: str = DEFAULT_MODEL):
        self.interface = interface
        self.model = normalize_model_name(model)
        
    def __call__(self, input_text: str) -> str:
        """Handle user input and return response."""
        try:
            response = litellm_completion(input_text, self.model)
            return response
        except Exception as e:
            self.interface.display_error(f"Error: {str(e)}")
            return "Sorry, I encountered an error."

    def __repr__(self) -> str:
        return f"Agent(model={self.model})"

class AgentAssert(Agent):
    """Concrete implementation of Agent for assertion testing."""
    
    def __init__(self, interface: UserInterface, model: str = DEFAULT_MODEL):
        super().__init__(interface, model)
        
    def __call__(self, input_text: str) -> str:
        """Handle user input and return response."""
        try:
            response = litellm_completion(input_text, self.model)
            return response
        except Exception as e:
            self.interface.display_error(f"Error: {str(e)}")
            return "Sorry, I encountered an error."
            
    def __repr__(self) -> str:
        return f"AgentAssert(model={self.model})"
