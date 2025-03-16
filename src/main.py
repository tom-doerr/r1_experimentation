from abc import ABC, abstractmethod
import subprocess
from typing import Any, Dict, Generator
import xml.etree.ElementTree as ET

import litellm

DEFAULT_MODEL: str = 'google/gemini-2.0-flash-001'
"""Default model to use for LiteLLM completion."""

def _validate_global_settings(settings: Dict[str, float]) -> None:
    """Validate global settings values."""
    required_keys = {'starting_cash', 'max_net_worth', 'min_net_worth', 'cash_penalty'}
    if not required_keys.issubset(settings.keys()):
        raise ValueError(f"Global settings must contain {required_keys}")
    
    if settings['min_net_worth'] < 0:
        raise ValueError("min_net_worth cannot be negative")
    if settings['max_net_worth'] <= settings['min_net_worth']:
        raise ValueError("max_net_worth must be greater than min_net_worth")
    if settings['starting_cash'] < settings['min_net_worth']:
        raise ValueError("starting_cash cannot be less than min_net_worth")
    if settings['starting_cash'] > settings['max_net_worth']:
        raise ValueError("starting_cash cannot exceed max_net_worth")
    if not 0 <= settings['cash_penalty'] <= 1:
        raise ValueError("cash_penalty must be between 0 and 1")

global_settings: Dict[str, float] = {
    'starting_cash': 1000.0,  # Default starting cash value
    'max_net_worth': 10000.0,  # Maximum allowed net worth
    'min_net_worth': 0.0,  # Minimum allowed net worth
    'cash_penalty': 0.1  # Percentage penalty for invalid operations
}

_validate_global_settings(global_settings)

def _parse_xml_value(element: ET.Element) -> str | bool | None:
    """Helper to parse XML element values."""
    if element.tag == 'bool':
        return element.text.lower() == 'true' if element.text else False
    return element.text if element.text is not None else ""

def _parse_xml_element(element: ET.Element) -> Dict[str, str | Dict[str, str] | None]:
    parsed_data = {}
    for child in element:
        if len(child) > 0:
            parsed_data[child.tag] = _parse_xml_element(child)
        else:
            parsed_data[child.tag] = _parse_xml_value(child)
    return parsed_data

def parse_xml(xml_string: str) -> Dict[str, str | Dict[str, str] | None]:
    """Parse XML string into a dictionary with proper error handling."""
    if not isinstance(xml_string, str) or not xml_string.strip():
        raise ValueError("XML string must be a non-empty string")
        
    try:
        root = ET.fromstring(xml_string)
        return {element.tag: _parse_xml_element(element) for element in root}
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}") from e


def python_reflection_testing() -> str:
    """Return sorted list of public function names in current module."""
    return ", ".join(sorted(
        name for name, obj in globals().items()
        if callable(obj) and not name.startswith('_')
    ))







class Tool(ABC):
    """Abstract base class for command execution tools."""
    
    @abstractmethod
    def run(self, command: str) -> str:
        """Execute a command and return the result.
        
        Args:
            command: The command string to execute
            
        Returns:
            Command output as string
            
        Raises:
            ValueError: If command is invalid
            RuntimeError: If execution fails
            NotImplementedError: If not implemented by subclass
        """
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
            raise ValueError(f"Command exceeds maximum length of {self.max_command_length}")
        if any(char in command for char in ['\n', '\r', '\0']):
            raise ValueError("Command contains invalid newline or null characters")
            
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

    def run(self, command: str) -> str:
        """Execute a shell command with strict validation."""
        self._validate_command(command)
            
        try:
            # Use shlex to properly handle quoted arguments
            import shlex
            result = subprocess.run(
                shlex.split(command),  # Properly handle quoted arguments
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


def litellm_completion(prompt: str, model: str, max_tokens: int = 100) -> str:
    """Generate completion using LiteLLM API with robust error handling."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model must be a non-empty string")
    if not isinstance(max_tokens, int) or max_tokens <= 0:
        raise ValueError("max_tokens must be a positive integer")
        
    model = _normalize_model_name(model)
        
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=max_tokens
        )
        if not response or not response.choices:
            raise RuntimeError("No response from API")
        return response.choices[0].message.content
    except litellm.exceptions.BadRequestError as e:
        if "not a valid model ID" in str(e):
            raise ValueError(f"Invalid model: {model}") from e
        raise RuntimeError(f"Bad request: {e}") from e
    except litellm.APIError as e:
        raise RuntimeError(f"API Error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}") from e

def _normalize_model_name(model: str) -> str:
    """Normalize model name to include proper provider prefix.
    
    Args:
        model: Raw model name string
        
    Returns:
        Normalized model name with openrouter/ prefix
    """
    if model.startswith('openrouter/'):
        return model
    if '/' in model:
        return f'openrouter/{model.split("/")[-1]}'
    return f'openrouter/{model}'
def _extract_content_from_chunks(response: Any) -> Generator[str, None, None]:
    """Extracts content from response chunks."""
    try:
        for chunk in response:
            if not chunk or not isinstance(chunk, dict):
                continue
            if "choices" not in chunk or not chunk["choices"]:
                continue
            if "delta" not in chunk["choices"][0]:
                continue
            if "content" not in chunk["choices"][0]["delta"]:
                continue
            content = chunk["choices"][0]["delta"]["content"]
            if content:  # Only yield non-empty content
                yield content
    except Exception as e:
        raise RuntimeError(f"Error extracting content: {e}") from e

def litellm_streaming(prompt: str, model: str = DEFAULT_MODEL, max_tokens: int = 100) -> Generator[str, None, None]:
    """Streaming version of litellm_completion that yields chunks of text."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model must be a non-empty string")
    if not isinstance(max_tokens, int) or max_tokens <= 0:
        raise ValueError("max_tokens must be a positive integer")
        
    model = _normalize_model_name(model)
        
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        for chunk in response:
            if chunk and isinstance(chunk, dict):
                if "choices" in chunk and chunk["choices"]:
                    if "delta" in chunk["choices"][0]:
                        if "content" in chunk["choices"][0]["delta"]:
                            content = chunk["choices"][0]["delta"]["content"]
                            if content:
                                yield content
    except litellm.exceptions.BadRequestError as e:
        if "not a valid model ID" in str(e):
            raise ValueError(f"Invalid model: {model}") from e
        raise RuntimeError(f"Bad request: {e}") from e
    except litellm.APIError as e:
        raise RuntimeError(f"API Error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}") from e







