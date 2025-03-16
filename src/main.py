import subprocess
from typing import Any, Dict, Generator
import xml.etree.ElementTree as ET
import litellm


DEFAULT_MODEL: str = 'openrouter/google/gemini-2.0-flash-001'  # Single definition
"""Default model to use for LiteLLM completion."""

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
                data[element.tag] = element.text if element.text is not None else ""
        return data
    except ET.ParseError as e:
        return {"error": str(e)}


def python_reflection_testing() -> str:
    return "test_output_var" # this is the expected return value, do not change







class Tool:
    """Base class for tools."""
    pass

class ShellCodeExecutor(Tool):
    """Executes shell commands safely with allow/deny lists."""
    blacklisted_commands = {'rm', 'cat', 'mv', 'cp'}
    whitelisted_commands = {'ls', 'date'}

    def __call__(self, command: str) -> str:
        return self.run(command)

    def __repr__(self):
        return "<ShellCodeExecutor>"

    def run(self, command: str) -> str:
        if not command:
            raise ValueError("No command provided")
        
        cmd = command.strip().split()[0]
        if cmd in self.blacklisted_commands:
            raise PermissionError(f"Command {cmd} not allowed")
        if cmd not in self.whitelisted_commands:
            raise ValueError(f"Command {cmd} not whitelisted")

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
        except subprocess.CalledProcessError as e:
            return f"Command failed: {e}"
        except Exception as e:
            return f"Error: {str(e)}"


def litellm_completion(prompt: str, model: str) -> str:
    """Completes the prompt using LiteLLM and returns the result."""
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )
        if not hasattr(response, 'choices') or not response.choices:
            raise ValueError(f"Unexpected response type: {type(response)}")
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            return response.choices[0].message.content
        raise ValueError("No content in response")
    except Exception as e:
        return f"LiteLLMError: {e}"
def _extract_content_from_chunks(response: Any) -> Generator[str, str, None]: # extracts content from response chunks.
    """Extracts content from response chunks."""
    try:
        for chunk in response:  # iterate over chunks
            yield chunk["choices"][0]["delta"]["content"]
    except (KeyError, litellm.APIError) as e:
        print(f"LiteLLMError in _extract_content_from_chunks: {e}")
        yield f"LiteLLMError: {e}"


def litellm_streaming(prompt: str, model: str = DEFAULT_MODEL, max_tokens: int = 100) -> Generator[str, str, None]: # streams the completion from LiteLLM
    response: Any = litellm.completion(model=model, messages=[{"role": "user", "content": prompt}], stream=True, max_tokens=max_tokens)
    yield from _extract_content_from_chunks(response)







