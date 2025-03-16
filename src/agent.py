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

    @staticmethod
    def assert_false(condition: bool, message: str = "") -> None:
        """Assert that a condition is false."""
        if condition:
            raise AssertionError(f"Condition not false: {message}")
    """Concrete agent implementation for testing assertions."""
    
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
        return f"AgentAssert(model={self.model!r}, max_tokens={self.max_tokens})"

