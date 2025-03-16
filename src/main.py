from typing import Any, Dict, Generator, Protocol
import xml.etree.ElementTree as ET

def parse_xml(xml_string: str) -> Dict[str, Any]:
    """Parse XML string into a dictionary."""
    try:
        root = ET.fromstring(xml_string)
        return {elem.tag: elem.text for elem in root}
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}") from e
import xml.etree.ElementTree as ET
from abc import abstractmethod
import xml.etree.ElementTree as ET
import subprocess
import shlex
import litellm
from .llm_utils import litellm_completion
from .config import DEFAULT_MODEL
from shutil import which  # Move this to top level import
from .config import DEFAULT_MODEL, global_settings
from .utils import normalize_model_name as _normalize_model_name
from .agent import Agent
from .interface import UserInterface
from .isolation import IsolatedEnvironment, run_container
from .reflection import python_reflection_test
from .envs import Env1, Env2
from .llm_utils import litellm_completion


def parse_xml(xml_string: str) -> Dict[str, Any]:
    """Parse XML string into a dictionary.
    
    Args:
        xml_string: XML string to parse
        
    Returns:
        Dict: Parsed XML data
        
    Raises:
        ValueError: If XML is invalid
    """
    try:
        root = ET.fromstring(xml_string)
        return {elem.tag: elem.text for elem in root}
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}") from e

def parse_xml(xml_string: str) -> Dict[str, Any]:
    """Parse XML string into dictionary.
    
    Args:
        xml_string: XML content to parse
        
    Returns:
        Dict: Parsed XML content as dictionary
        
    Raises:
        ValueError: If XML is invalid
    """
    try:
        root = ET.fromstring(xml_string)
        return {elem.tag: elem.text for elem in root}
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}") from e

def _validate_global_settings(settings: Dict[str, float]) -> None:
    """Validate global settings values."""
    required_keys = {'starting_cash', 'max_net_worth', 'min_net_worth', 'cash_penalty'}
    if not isinstance(settings, dict):
        raise TypeError("settings must be a dictionary")
    if not all(key in settings for key in required_keys):
        raise ValueError(f"settings must contain all required keys: {required_keys}")
    if not all(isinstance(v, (int, float)) for v in settings.values()):
        raise TypeError("All settings values must be numeric")
















def parse_xml(xml_string: str) -> ET.Element:
    """Parse XML string and return ElementTree element."""
    try:
        return ET.fromstring(xml_string)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {str(e)}") from e

class Tool(Protocol):
    """Protocol defining interface for command execution tools."""
    
    @abstractmethod
    def run(self, command: str) -> str:
        """Execute a command and return the result."""
        raise NotImplementedError
        
    @abstractmethod 
    def __call__(self, command: str) -> str:
        """Make tool callable for convenience."""
        return self.run(command)
        
    @abstractmethod
    def __repr__(self) -> str:
        """Return string representation of tool."""
        return f"{self.__class__.__name__}()"
        
    @property
    @abstractmethod
    def is_available(self) -> bool:
        """Check if tool is available for use."""
        raise NotImplementedError

class ShellCodeExecutor(Tool):
    """Safely executes whitelisted shell commands with strict validation."""
    blacklisted_commands = {'rm', 'cat', 'mv', 'cp', 'sudo', 'sh', 'bash', 'wget', 'curl', 'ssh'}
    whitelisted_commands = {'ls', 'date', 'pwd', 'echo', 'whoami', 'uname', 'hostname'}
    max_command_length = 100
    
    def __call__(self, command: str) -> str:
        return self.run(command)

    def __repr__(self) -> str:
        return f"ShellCodeExecutor(whitelist={self.whitelisted_commands})"
        
    @property
    def is_available(self) -> bool:
        """Check if shell commands can be executed."""
        return which('sh') is not None  # Simplified since we moved import to top

    def _validate_command(self, command: str) -> None:
        """Validate command before execution."""
        if not isinstance(command, str) or not command.strip():
            raise ValueError("Command must be a non-empty string")
        if any(char in command for char in ['\n', '\r', '\0', ';', '|', '&', '`', '$', '(', ')', '>', '<']):
            raise ValueError(f"Command contains invalid characters: {command}")
        if len(command) > self.max_command_length:
            raise ValueError(f"Command exceeds maximum length of {self.max_command_length} characters")
            
        parts = command.strip().split()
        if not parts:
            raise ValueError("Empty command")
            
        cmd = parts[0]
        if cmd in self.blacklisted_commands:
            raise PermissionError(f"Command {cmd} is blacklisted")
        if cmd not in self.whitelisted_commands:
            raise ValueError(f"Command {cmd} is not whitelisted")
            
        # Additional validation for command arguments
        if len(parts) > 1:
            for arg in parts[1:]:
                if any(char in arg for char in ['\n', '\r', '\0', ';', '|', '&', '`', '$', '(', ')', '>', '<']):
                    raise ValueError(f"Invalid character in argument: {arg}")

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


































def litellm_streaming(prompt: str, model: str, max_tokens: int = 100) -> Generator[str, None, None]:
    """Generate streaming completion using LiteLLM API.
    
    Args:
        prompt: The input prompt string
        model: The model name to use
        max_tokens: Maximum number of tokens to generate
        
    Yields:
        str: Chunks of the generated completion
        
    Raises:
        ValueError: If inputs are invalid
        RuntimeError: If completion fails
    """
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string")
        
    try:
        model = normalize_model_name(model)
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            stream=True
        )
        
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content
                
    except Exception as e:
        raise RuntimeError(f"Streaming error: {e}") from e

def python_reflection_test(obj: object) -> str:
    """Inspect an object and return its type information."""
    if obj is None:
        return "None"
    return f"{type(obj).__name__}: {dir(obj)}"










__all__ = [
    "parse_xml", "Tool", "ShellCodeExecutor", "python_reflection_test",
    "litellm_completion", "litellm_streaming", "DEFAULT_MODEL", "global_settings",
    "IsolatedEnvironment", "run_container", "UserInterface",
    "Env1", "Env2", "Agent", "AgentAssert"
]



