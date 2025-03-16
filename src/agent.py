from typing import Any, Dict, Protocol
from abc import abstractmethod, ABC
from .llm_utils import litellm_completion
from .config import DEFAULT_MODEL, global_settings
from .interface import UserInterface, ConsoleInterface
from .utils import normalize_model_name

class Agent(ABC):



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

