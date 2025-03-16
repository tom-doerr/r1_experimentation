from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .agent import Agent

class UserInterface:
    """Concrete implementation of user interface."""
    
    def display_message(self, message: str) -> None:
        """Display a message to the user"""
        print(message)
        
    def display_error(self, error: str) -> None:
        """Display an error message to the user."""
        print(f"Error: {error}")
        
    def get_input(self, prompt: str) -> str:
        """Get input from the user."""
        return input(prompt)
        
    def interact_with_agent(self, agent: 'Agent') -> None:
        """Interact with an agent instance."""
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
                
    def __repr__(self) -> str:
        """Return string representation for reflection test."""
        return f"{self.__class__.__name__}()"

class ConsoleInterface(UserInterface):
    """Concrete implementation of UserInterface for console interaction."""
    
    def __init__(self):
        super().__init__()
        self.running = False
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
