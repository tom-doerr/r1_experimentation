from typing import Protocol
from .agent import Agent

class UserInterface(Protocol):
    """Protocol defining the interface for user interaction."""
    
    def display_message(self, message: str) -> None:
        """Display a message to the user."""
        ...
        
    def get_input(self, prompt: str) -> str:
        """Get input from the user."""
        ...
        
    def interact_with_agent(self, agent: Agent) -> None:
        """Interact with an agent instance."""
        ...
