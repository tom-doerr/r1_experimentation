import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, Generator
import litellm

FLASH: str = 'openrouter/google/gemini-2.0-flash-001'

def parse_xml(xml_string: str) -> Dict[str, Any]:
    """Parses an XML string and returns a dictionary."""
    try:
        root = ET.fromstring(xml_string)
        return _parse_element(root)
    except ET.ParseError as e:
        print(f"Invalid XML: {e}")
        return {}

def _parse_element(element: ET.Element) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for child in element:
        if len(child) == 0:
            child_data: Any = child.text.strip() if child.text is not None else ""
        else:
            child_data: Any = _parse_element(child)

        if child.tag in result:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            result[child.tag].append(child_data)
        else:
            result[child.tag] = child_data
    return result

def litellm_completion(prompt: str, model: str) -> str:
    """Uses the litellm library to get a completion."""
    messages = [{"role": "user", "content": prompt}]
    try:
        response = litellm.completion(model=model, messages=messages)
        if response and response.choices and response.choices[0].message:
            return response.choices[0].message.content
        return ""
    except litellm.LiteLLMError as e:
        print(f"LiteLLMError during litellm completion: {type(e).__name__} - {e}")
        return ""
    except Exception as e:
        print(f"General error during litellm completion: {type(e).__name__} - {e}")
        return ""


def litellm_streaming(prompt: str, model: str = FLASH, max_tokens: Optional[int] = None) -> Generator[str, None, None]:
    """Uses the litellm library to stream a completion."""
    messages = [{"role": "user", "content": prompt}]
    kwargs: Dict[str, Any] = {"model": model, "messages": messages, "stream": True}
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens
    try:
        response = litellm.completion(**kwargs)
        if isinstance(response, dict):  # Handle non-streaming response
            if 'choices' in response and len(response['choices']) > 0 and 'message' in response['choices'][0]:
                yield response['choices'][0]['message']['content']
            else:
                print(f"Unexpected non-streaming response format: {response}")
                yield ""
        else:  # Handle streaming response
            for chunk in response:
                if 'choices' in chunk and len(chunk['choices']) > 0 and 'delta' in chunk['choices'][0] and 'content' in chunk['choices'][0]['delta']:
                    content = chunk['choices'][0]['delta']['content']
                    yield content
                else:
                    print(f"Unexpected chunk format: {chunk}")
                    yield ""
    except litellm.LiteLLMError as e:
        print(f"LiteLLMError during litellm streaming: {type(e).__name__} - {e}")
        yield ""
    except Exception as e:
        print(f"General error during litellm streaming: {type(e).__name__} - {e}")
        yield ""

def python_reflection_testing() -> str:
    """Returns a test string for reflection testing."""
    return "test_output_var"

def test_env_1(input_str: str) -> int:
    if 'aaa' in input_str:
        return 3
    return 4

class Agent:
    def __init__(self, model: str = FLASH):
        self.model: str = model
        self.memory: str = ""
        self.last_completion: str = ""

    def reply(self, prompt: str) -> str:
        self.last_completion: str = litellm_completion(prompt, self.model)
        return self.last_completion

    def _parse_xml(self, xml_string: str) -> Dict[str, Any]:
        return parse_xml(xml_string)

    def _update_memory(self, search: str, replace: str) -> None:
        self.memory = replace if replace is not None else ""

class AgentAssert:
    """Assertion agent for testing."""
    def __init__(self, model: str):
        self.agent: Agent = Agent(model=model)

    def _parse_xml(self, xml_string: str) -> bool:
        parsed: Dict[str, Any] = parse_xml(xml_string)
        if 'bool' in parsed:
            bool_value: str = parsed['bool']
            return bool_value.lower() == 'true'
        return False
