from __future__ import annotations
from abc import abstractmethod
from typing import Protocol, TYPE_CHECKING
if TYPE_CHECKING:
    from .agent import Agent

class UserInterface(Protocol):
    """Protocol defining the interface for user interaction."""
    
    @abstractmethod
    def display_message(self, message: str) -> None:
        """Display a message to the user"""
        
    @abstractmethod
    def display_error(self, error: str) -> None:
        """Display a message to the user."""
        
    @abstractmethod
    def get_input(self, prompt: str) -> str:
        """Get input from the user."""
        ...  # Abstract method - implementation required
    def interact_with_agent(self, agent: 'Agent') -> None:
        """Interact with an agent instance."""

class ConsoleInterface(UserInterface):
    """Concrete implementation of UserInterface for console interaction."""
    
    def display_message(self, message: str) -> None:
        print(message)
        
    def display_error(self, error: str) -> None:
        print(f"Error: {error}")
        
    def get_input(self, prompt: str) -> str:
        return input(prompt)
        
    def interact_with_agent(self, agent: 'Agent') -> None:
        while True:
            user_input = self.get_input("You: ")
            if user_input.lower() in ('exit', 'quit'):
                break
            response = agent(user_input)
            self.display_message(f"Agent: {response}")
