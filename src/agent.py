from typing import Any
from abc import ABC
from .llm_utils import litellm_completion
from .config import DEFAULT_MODEL
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

    @staticmethod
    def assert_false(condition: bool, message: str = "") -> None:
        """Assert that a condition is false."""
        if condition:
            raise AssertionError(f"Condition not false: {message}")

