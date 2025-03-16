from abc import ABC, abstractmethod
import subprocess
from typing import Any, Dict, Generator
import xml.etree.ElementTree as ET

import litellm

DEFAULT_MODEL: str = 'google/gemini-2.0-flash-001'
"""Default model to use for LiteLLM completion."""

global_settings = {
    'starting_cash': 1000.0  # Default starting cash value
}

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
    try:
        root: ET.Element = ET.fromstring(xml_string)
        data: Dict[str, str | Dict[str, str] | None] = {}
        for element in root:
            if list(element):
                data[element.tag] = _parse_xml_element(element)
            else:
                data[element.tag] = _parse_xml_value(element)
        return data
    except ET.ParseError as e:
        return {"error": str(e)}


def python_reflection_testing() -> str:
    """Return sorted list of function names in current module."""
    current_module = __import__(__name__)
    return ", ".join(sorted(
        name for name, obj in vars(current_module).items()
        if callable(obj) and not name.startswith('_')
    ))







class Tool(ABC):
    """Abstract base class for command execution tools.
    
    Subclasses must implement the run() method to execute commands.
    """
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

class ShellCodeExecutor(Tool):
    """Safely executes whitelisted shell commands with strict validation.
    
    Attributes:
        blacklisted_commands: Set of forbidden commands
        whitelisted_commands: Set of allowed commands
        max_command_length: Maximum allowed command length
    """
    blacklisted_commands = {'rm', 'cat', 'mv', 'cp', 'sudo', 'sh', 'bash'}
    whitelisted_commands = {'ls', 'date', 'pwd', 'echo', 'whoami'}
    max_command_length = 100
    
    def __call__(self, command: str) -> str:
        return self.run(command)

    def __repr__(self) -> str:
        return "<ShellCodeExecutor>"

    def run(self, command: str) -> str:
        """Execute a shell command with strict validation.
        
        Args:
            command: Command string to execute
            
        Returns:
            Command output as string
            
        Raises:
            ValueError: For invalid commands or arguments
            PermissionError: For blacklisted commands
            RuntimeError: For execution failures
            TimeoutError: If command times out
        """
        # Validate command format
        if not isinstance(command, str) or not command.strip():
            raise ValueError("Command must be a non-empty string")
        if len(command) > self.max_command_length:
            raise ValueError(f"Command exceeds maximum length of {self.max_command_length}")
            
        # Split and validate command parts
        parts = command.strip().split()
        if not parts:
            raise ValueError("Empty command")
            
        cmd = parts[0]
        if cmd in self.blacklisted_commands:
            raise PermissionError(f"Command {cmd} is blacklisted")
        if cmd not in self.whitelisted_commands:
            raise ValueError(f"Command {cmd} is not whitelisted")
            
        # Validate arguments for security
        if len(parts) > 1:
            for arg in parts[1:]:
                if any(char in arg for char in [';', '|', '&', '`', '$', '(', ')', '>', '<']):
                    raise ValueError(f"Invalid characters in argument: {arg}")
                if '..' in arg:  # Prevent path traversal
                    raise ValueError("Path traversal detected in arguments")
            
        try:
            result = subprocess.run(
                command,
                shell=True,
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
    """Generate completion using LiteLLM API with robust error handling.
    
    Args:
        prompt: Non-empty string prompt to send to the model
        model: Model identifier string (with or without provider prefix)
        max_tokens: Positive integer for maximum tokens to generate
        
    Returns:
        Generated text completion
        
    Raises:
        ValueError: For invalid inputs or model names
        RuntimeError: For API or execution errors
    """
    # Validate inputs
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model must be a non-empty string")
    if not isinstance(max_tokens, int) or max_tokens <= 0:
        raise ValueError("max_tokens must be a positive integer")
        
    # Normalize model name format
    model = _normalize_model_name(model)
        
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=max_tokens
        )
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
            if "choices" not in chunk or not chunk["choices"]:
                raise ValueError("Invalid response format from LiteLLM")
            yield chunk["choices"][0]["delta"]["content"]
    except KeyError as e:
        raise ValueError(f"Invalid response format: {e}") from e
    except litellm.APIError as e:
        raise RuntimeError(f"API Error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error: {e}") from e


def litellm_streaming(prompt: str, model: str = DEFAULT_MODEL, max_tokens: int = 100) -> Generator[str, None, None]:
    if not prompt or not isinstance(prompt, str):
        raise ValueError("Prompt must be a non-empty string")
    if not model or not isinstance(model, str):
        raise ValueError("Model must be a non-empty string")
    if not isinstance(max_tokens, int) or max_tokens <= 0:
        raise ValueError("max_tokens must be a positive integer")
        
    # Handle model prefix like litellm_completion
    if model.startswith('openrouter/'):
        pass
    elif '/' in model:
        model = f'openrouter/{model.split("/")[-1]}'
    else:
        model = f'openrouter/{model}'
        
    try:
        response: Any = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=max_tokens
        )
        yield from _extract_content_from_chunks(response)
    except litellm.APIError as e:
        raise RuntimeError(f"API Error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error: {e}") from e







