from typing import Any, Dict, Protocol
from abc import abstractmethod
from abc import abstractmethod
from abc import abstractmethod
from .llm_utils import litellm_completion
from .config import DEFAULT_MODEL

class Agent:
    """Main agent class that handles interactions and commands."""
    
    def __init__(self, interface: UserInterface, model: str = DEFAULT_MODEL):
        self.interface = interface
        self.model = model
        
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
