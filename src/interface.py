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
        """Display an error message to the user."""
        
    @abstractmethod
    def get_input(self, prompt: str) -> str:
        """Get input from the user."""
        
    def interact_with_agent(self, agent: 'Agent') -> None:
        """Interact with an agent instance."""

class ConsoleInterface(UserInterface):
    """Concrete implementation of UserInterface for console interaction."""
    
    def __init__(self):
        self.running = False
        
    def display_message(self, message: str) -> None:
        print(f"Agent: {message}")
        
    def display_error(self, error: str) -> None:
        print(f"Error: {error}")
        
    def get_input(self, prompt: str) -> str:
        return input(prompt)
        
    def interact_with_agent(self, agent: 'Agent') -> None:
        self.running = True
        while self.running:
            try:
                user_input = self.get_input("You: ")
                if user_input.lower() in ('exit', 'quit'):
                    self.running = False
                    break
                response = agent(user_input)
                self.display_message(response)
            except Exception as e:
                self.display_error(str(e))
