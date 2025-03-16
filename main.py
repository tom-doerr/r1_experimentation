import xml.etree.ElementTree as ET
from typing import Dict, Any, Generator, Optional
import litellm

FLASH = 'openrouter/google/gemini-2.0-flash-001'

def parse_xml(xml_string: str):
    try:
        root = ET.fromstring(xml_string)
        return _parse_element(root)
    except ET.ParseError as e:
        print(f"Invalid XML: {e}")
        return {}

def _parse_element(element: ET.Element) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for child in element:
        child_data: Any = {}
        if child.text:
            child_data = child.text.strip()
        else:
            child_data = _parse_element(child)
        result[child.tag] = child_data
    return result

def litellm_completion(prompt: str, model: str):
    """Uses the litellm library to get a completion."""
    messages = [{"role": "user", "content": prompt}]
    try:
        response = litellm.completion(model=model, messages=messages)
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content
        return ""
    except Exception as e:
        print(f"Error during litellm completion: {type(e).__name__} - {e}")
        return ""


def litellm_streaming(prompt: str, model: str = FLASH, max_tokens: Optional[int] = None):
    messages = [{"role": "user", "content": prompt}]
    kwargs = {"model": model, "messages": messages, "stream": True}
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens
    try:
        response = litellm.completion(**kwargs)
        if hasattr(response, 'choices'):
            for choice in response.choices:
                if choice.delta and choice.delta.content:
                    yield choice.delta.content
        else:
            print("Unexpected response format: ", response)
            yield ""
    except Exception as e:
        print(f"Error during litellm streaming: {type(e).__name__} - {e}")
        yield ""

def python_reflection_testing():
    return "test_output_var"

def test_env_1(input_str: str):
    if 'aaa' in input_str:
        return 3
    return 4

FLASH = 'openrouter/google/gemini-2.0-flash-001'

class Agent:
    def __init__(self, model: str = FLASH):
        self.model: str = model
        self.memory: str = ""
        self.last_completion: str = ""

    def reply(self, prompt: str):
        self.last_completion: str = litellm_completion(prompt, self.model)
        return self.last_completion

    def _parse_xml(self, xml_string: str):
        return parse_xml(xml_string)

    def _update_memory(self, search: str, replace: str):
        self.memory: str = replace

class AgentAssert:
    """Assertion agent for testing."""
    def __init__(self, model: str):
        self.agent: Agent = Agent(model=model)

    def _parse_xml(self, xml_string: str):
        parsed = parse_xml(xml_string)
        if 'response' in parsed and 'bool' in parsed['response']:
            bool_value = parsed['response']['bool']
            return bool_value.lower() == 'true'
        # Return False if 'response' or 'bool' is missing, indicating a failed assertion
        return False
