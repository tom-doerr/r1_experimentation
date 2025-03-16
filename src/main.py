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

def _parse_xml_element(element: ET.Element) -> Dict[str, str | Dict[str, str] | None]:
    parsed_data = {}
    for child in element:
        if len(child) > 0:
            parsed_data[child.tag] = _parse_xml_element(child)
        else:
            # Convert boolean values
            if child.tag == 'bool':
                parsed_data[child.tag] = child.text.lower() == 'true' if child.text else False
            else:
                parsed_data[child.tag] = child.text
    return parsed_data

def parse_xml(xml_string: str) -> Dict[str, str | Dict[str, str] | None]:
    try:
        root: ET.Element = ET.fromstring(xml_string)
        data: Dict[str, str | Dict[str, str] | None] = {}
        for element in root:
            if list(element):
                data[element.tag] = _parse_xml_element(element)
            else:
                # Handle empty elements and boolean values
                if element.tag == 'bool':
                    data[element.tag] = element.text.lower() == 'true' if element.text else False
                else:
                    data[element.tag] = element.text if element.text is not None else ""
        return data
    except ET.ParseError as e:
        return {"error": str(e)}


def python_reflection_testing() -> str:
    """Return sorted list of function names in current module."""
    import inspect
    import sys
    return ", ".join(sorted(
        name for name, obj in inspect.getmembers(sys.modules[__name__])
        if inspect.isfunction(obj)
    ))







class Tool(ABC):
    """Base class for tools that execute commands."""
    @abstractmethod
    def run(self, command: str) -> str:
        """Execute a command and return the result.
        
        Args:
            command: The command to execute
            
        Returns:
            str: The result of executing the command
            
        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement run()")

class ShellCodeExecutor(Tool):
    """Executes shell commands safely with allow/deny lists."""
    blacklisted_commands = {'rm', 'cat', 'mv', 'cp', 'sudo', 'sh', 'bash'}
    whitelisted_commands = {'ls', 'date', 'pwd', 'echo', 'whoami'}
    
    def __call__(self, command: str) -> str:
        return self.run(command)

    def __repr__(self):
        return "<ShellCodeExecutor>"

    def run(self, command: str) -> str:
        if not isinstance(command, str) or not command.strip():
            raise ValueError("Command must be a non-empty string")
            
        # Split command and validate each part
        parts = command.strip().split()
        if not parts:
            raise ValueError("Empty command")
            
        cmd = parts[0]
        if cmd in self.blacklisted_commands:
            raise PermissionError(f"Command {cmd} is blacklisted")
        if cmd not in self.whitelisted_commands:
            raise ValueError(f"Command {cmd} is not whitelisted")
            
        # Validate arguments
        if len(parts) > 1:
            for arg in parts[1:]:
                if any(char in arg for char in [';', '|', '&', '`', '$', '(', ')']):
                    raise ValueError(f"Invalid characters in argument: {arg}")
            
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
        except subprocess.TimeoutExpired:
            raise TimeoutError("Command timed out")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Command failed: {e.stderr}") from e
        except Exception as e:
            raise RuntimeError(f"Error executing command: {e}") from e


def litellm_completion(prompt: str, model: str, max_tokens: int = 100) -> str:
    # Validate inputs
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model must be a non-empty string")
    if not isinstance(max_tokens, int) or max_tokens <= 0:
        raise ValueError("max_tokens must be a positive integer")
        
    # Handle model prefix based on provider
    if model.startswith('openrouter/'):
        # Already has correct prefix
        pass
    elif '/' in model:
        # Has provider prefix but not openrouter
        model = f'openrouter/{model.split("/")[-1]}'
    else:
        # No prefix at all
        model = f'openrouter/{model}'
        
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
        raise
    except litellm.APIError as e:
        raise RuntimeError(f"API Error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error: {e}") from e
def _extract_content_from_chunks(response: Any) -> Generator[str, str, None]: # extracts content from response chunks.
    """Extracts content from response chunks."""
    try:
        for chunk in response:  # iterate over chunks
            yield chunk["choices"][0]["delta"]["content"]
    except (KeyError, litellm.APIError) as e:
        print(f"LiteLLMError in _extract_content_from_chunks: {e}")
        yield f"LiteLLMError: {e}"


def litellm_streaming(prompt: str, model: str = DEFAULT_MODEL, max_tokens: int = 100) -> Generator[str, str, None]:
    if not prompt or not isinstance(prompt, str):
        raise ValueError("Prompt must be a non-empty string")
    if not model or not isinstance(model, str):
        raise ValueError("Model must be a non-empty string")
    if not isinstance(max_tokens, int) or max_tokens <= 0:
        raise ValueError("max_tokens must be a positive integer")
        
    try:
        response: Any = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=max_tokens
        )
        yield from _extract_content_from_chunks(response)
    except litellm.APIError as e:
        yield f"API Error: {e}"
    except Exception as e:
        yield f"Error: {e}"







