from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, List, Protocol
import inspect
import shlex
import subprocess
import xml.etree.ElementTree as ET
import litellm
from .isolation import run_container

DEFAULT_MODEL = "openrouter/google/gemini-2.0-flash-001"

global_settings = {
    'starting_cash': 1000.0,
    'max_net_worth': 10000.0,
    'min_net_worth': 0.0,
    'cash_penalty': 0.1,
    'initial_net_worth': 1000.0
}




def _validate_global_settings(settings: Dict[str, float]) -> None:
    """Validate global settings values."""
    required_keys = {'starting_cash', 'max_net_worth', 'min_net_worth', 'cash_penalty'}
    if not isinstance(settings, dict):
        raise TypeError("settings must be a dictionary")
    if not all(key in settings for key in required_keys):
        raise ValueError(f"settings must contain all required keys: {required_keys}")
    if not all(isinstance(v, (int, float)) for v in settings.values()):
        raise TypeError("All settings values must be numeric")


def _parse_xml_value(element: ET.Element) -> str | bool:
    """Parse XML element value."""
    if element.tag == 'bool':
        return element.text and element.text.lower() == 'true'
    return element.text or ""

def _parse_xml_element(element: ET.Element) -> Dict[str, Any]:
    """Parse XML element and its children."""
    return {
        child.tag: _parse_xml_element(child) if len(child) > 0 
        else _parse_xml_value(child)
        for child in element
    }

def parse_xml(xml_string: str) -> Dict[str, str | Dict[str, str] | None]:
    """Parse XML string into a dictionary with proper error handling.
    
    Args:
        xml_string: The XML string to parse
        
    Returns:
        Dictionary containing parsed XML data
        
    Raises:
        ValueError: If XML string is invalid or empty
    """
    if not isinstance(xml_string, str) or not xml_string.strip():
        raise ValueError("XML string must be a non-empty string")
        
    try:
        root = ET.fromstring(xml_string)
        return {element.tag: _parse_xml_element(element) for element in root}
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}") from e









class Tool(ABC):
    """Abstract base class for command execution tools."""
    
    @abstractmethod
    def run(self, command: str) -> str:
        """Execute a command and return the result."""
        raise NotImplementedError("Subclasses must implement run()")
        
    @abstractmethod 
    def __call__(self, command: str) -> str:
        """Make tool callable for convenience."""
        raise NotImplementedError("Subclasses must implement __call__")
        
    @abstractmethod
    def __repr__(self) -> str:
        """Return string representation of tool."""
        raise NotImplementedError("Subclasses must implement __repr__")

class ShellCodeExecutor(Tool):
    """Safely executes whitelisted shell commands with strict validation."""
    blacklisted_commands = {'rm', 'cat', 'mv', 'cp', 'sudo', 'sh', 'bash', 'wget', 'curl', 'ssh'}
    whitelisted_commands = {'ls', 'date', 'pwd', 'echo', 'whoami', 'uname', 'hostname'}
    max_command_length = 100
    
    def __call__(self, command: str) -> str:
        return self.run(command)

    def __repr__(self) -> str:
        return "<ShellCodeExecutor>"

    def _validate_command(self, command: str) -> None:
        """Validate command before execution."""
        if not isinstance(command, str) or not command.strip():
            raise ValueError("Command must be a non-empty string")
        if len(command) > self.max_command_length:
            raise ValueError(f"Command exceeds maximum length of {self.max_command_length} characters")
        if any(char in command for char in ['\n', '\r', '\0']):
            raise ValueError("Command contains invalid control characters (newline or null)")
            
        parts = command.strip().split()
        if not parts:
            raise ValueError("Empty command")
            
        cmd = parts[0]
        if cmd in self.blacklisted_commands:
            raise PermissionError(f"Command {cmd} is blacklisted")
        if cmd not in self.whitelisted_commands:
            raise ValueError(f"Command {cmd} is not whitelisted")
            
        if len(parts) > 1:
            for arg in parts[1:]:
                if any(char in arg for char in [';', '|', '&', '`', '$', '(', ')', '>', '<']):
                    raise ValueError(f"Invalid characters in argument: {arg}")
                if '..' in arg:
                    raise ValueError("Path traversal detected in arguments")
                if arg.startswith('-'):
                    raise ValueError("Arguments cannot start with hyphens")
                if len(arg) > 50:
                    raise ValueError("Argument too long")

    def run(self, command: str) -> str:
        """Execute a shell command with strict validation."""
        self._validate_command(command)
            
        try:
            result = subprocess.run(
                shlex.split(command),
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            return result.stdout
        except subprocess.TimeoutExpired as e:
            raise TimeoutError("Command timed out") from e
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command failed: {e.stderr}") from e
        except Exception as e:
            raise RuntimeError(f"Error executing command: {e}") from e
























def _execute_command(command: str, timeout: int = 10) -> str:
    """Execute a shell command and return the output.
    
    Args:
        command: The command string to execute
        timeout: Maximum execution time in seconds
        
    Returns:
        Command output as string
        
    Raises:
        ValueError: If command is invalid
        RuntimeError: If execution fails
    """
    if not isinstance(command, str) or not command.strip():
        raise ValueError("Command must be a non-empty string")
    if not isinstance(timeout, int) or timeout <= 0:
        raise ValueError("Timeout must be a positive integer")
        
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout
        )
        return result.stdout
    except subprocess.TimeoutExpired as e:
        raise TimeoutError(f"Command timed out after {timeout} seconds") from e
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {e.stderr}") from e
    except Exception as e:
        raise RuntimeError(f"Error executing command: {e}") from e

def python_reflection_test(obj: Any) -> Dict[str, Any]:
    """Inspect a Python object and return its attributes and methods.
    
    Args:
        obj: Any Python object to inspect
        
    Returns:
        Dictionary containing:
            - type: The object's type
            - attributes: Dictionary of instance attributes
            - methods: List of method names
            
    Raises:
        ValueError: If obj is None
    """
    if obj is None:
        raise ValueError("Cannot inspect None object")
        
    result = {
        'type': str(type(obj)),
        'attributes': {},
        'methods': []
    }
    
    # Get instance attributes
    for name, value in vars(obj).items():
        result['attributes'][name] = str(value)
        
    # Get methods
    for name in dir(obj):
        if callable(getattr(obj, name)) and not name.startswith('_'):
            result['methods'].append(name)
            
    return result

def _normalize_model_name(model: str) -> str:
    """Normalize model name to include proper provider prefix.
    
    Args:
        model: Raw model name string
        
    Returns:
        Normalized model name with proper prefix
        
    Raises:
        ValueError: If model name is invalid
    """
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model must be a non-empty string")
        
    model = model.strip().lower()
    
    # Handle flash alias
    if model == "flash":
        return "openrouter/google/gemini-2.0-flash-001"
        
    # Handle deepseek models
    if model == "deepseek":
        return "deepseek/deepseek-chat"
    if model.startswith("deepseek/"):
        return model
        
    # Handle openrouter models
    if model.startswith("openrouter/"):
        return model
        
    # Handle other models
    if "/" in model:
        return f"openrouter/{model}"
        
    return f"openrouter/{model}"

def litellm_completion(prompt: str, model: str, max_tokens: int = 100) -> str:
    """Generate completion using LiteLLM API with robust error handling.
    
    Args:
        prompt: The input prompt string
        model: The model name to use
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        str: The generated completion
        
    Raises:
        ValueError: If inputs are invalid
        RuntimeError: If completion fails
    """






























def python_reflection_test() -> str:
    """Test Python reflection capabilities.
    
    Returns:
        str: A string containing reflection test results
    """
    import inspect
    import sys
    
    results = []
    
    # Test module inspection
    current_module = sys.modules[__name__]
    results.append(f"Module name: {current_module.__name__}")
    
    # Test function inspection
    functions = inspect.getmembers(current_module, inspect.isfunction)
    results.append(f"Found {len(functions)} functions")
    
    # Test class inspection
    classes = inspect.getmembers(current_module, inspect.isclass)
    results.append(f"Found {len(classes)} classes")
    
    return "\n".join(results)
