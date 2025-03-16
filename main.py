import xml.etree.ElementTree as ET
from typing import Dict, Any, Generator, Optional
import os
import litellm

def parse_xml(xml_string: str) -> Dict[str, Any]:
    """XML parser with nested structure support"""
    try:
        root = ET.fromstring(xml_string)
        return _parse_element(root)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}") from e

def _parse_element(element: ET.Element) -> Dict[str, Any]:
    result: Dict[str, Any] = {}

    for child in element:
        child_data = _parse_element(child)
        if child.tag in result:
            if isinstance(result[child.tag], list):
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data

    if element.text and element.text.strip() and not result:
        result['message'] = element.text.strip()

    return {element.tag: result} if result else element.text.strip() if element.text else {}

def litellm_completion(prompt: str, model: str) -> str:
    """Uses the litellm library to get a completion."""
    messages = [{"role": "user", "content": prompt}]
    try:
        response = litellm.completion(model=model, messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error during litellm completion: {e}")
        return ""  # Or handle the error as appropriate

def litellm_streaming(prompt: str, model: str, max_tokens: Optional[int] = None) -> Generator[str, None, None]:
    """Uses the litellm library to stream a completion."""
    messages = [{"role": "user", "content": prompt}]
    arguments = {"model": model, "messages": messages, "stream": True}
    if max_tokens is not None:
        arguments["max_tokens"] = max_tokens

    response = litellm.completion(**arguments)

    for chunk in response:
        for choice in chunk.choices:
            if choice.delta and choice.delta.content:
                yield choice.delta.content

def python_reflection_testing() -> str:
    """Placeholder for python reflection testing."""
    return "test_output_var"

def test_env_1(input_str: str) -> int:
    """Placeholder for test environment 1."""
    if 'aaa' in input_str:
        return 3
    else:
        return 4

class Agent:
    """Placeholder for Agent class."""
    def __init__(self, model: str):
        self.model = model
        self.memory = ""
        self.last_completion = ""

    def reply(self, prompt: str) -> str:
        """Placeholder reply method."""
        self.last_completion = litellm_completion(prompt, self.model)
        return self.last_completion

    def _parse_xml(self, xml_string: str) -> Dict[str, Any]:
        """XML parsing."""
        return parse_xml(xml_string)

    def _update_memory(self, search: str, replace: str) -> None:
        """Updates the agent's memory."""
        self.memory = replace

class AgentAssert:
    """Placeholder for AgentAssert class."""
    def __init__(self, model: str):
        self.agent = Agent(model=model)

    def _parse_xml(self, xml_string: str) -> bool:
        """XML parsing that returns a boolean."""
        if "False" in xml_string:
            return False
        return True
