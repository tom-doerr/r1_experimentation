from typing import Any
from abc import ABC, abstractmethod
from .config import DEFAULT_MODEL
from .interface import UserInterface
from .interface import UserInterface

class Agent(ABC):
    """Abstract base class for agents."""
    
    def __init__(self, interface: UserInterface, model: str = DEFAULT_MODEL, max_tokens: int = 100):
        """Initialize agent with interface and model settings."""
        self.interface = interface
        self.model = model
        self.max_tokens = max_tokens



    @abstractmethod
    def __call__(self, input_text: str) -> str:
        """Process input and return response."""
        pass

    @staticmethod
    def assert_equal(actual: Any, expected: Any, message: str = "") -> None:
        """Assert that two values are equal."""
        if actual != expected:
            raise AssertionError(f"{message}\nExpected: {expected}\nActual: {actual}")

    @staticmethod
    def assert_true(condition: bool, message: str = "") -> None:
        """Assert that a condition is true."""
        if not condition:
            raise AssertionError(f"Condition not true: {message}")


class Agent(ABC):
    """Concrete agent implementation."""
    
    def __init__(self, interface: UserInterface, model: str = DEFAULT_MODEL, max_tokens: int = 100):
        self.interface = interface
        self.model = model
        self.max_tokens = max_tokens
        
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
        return f"Agent(model={self.model!r}, max_tokens={self.max_tokens})"

