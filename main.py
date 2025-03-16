import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, Generator, List
import litellm

FLASH: str = 'openrouter/google/gemini-2.0-flash-001'
# Set flash as the default model
litellm.model_list = [{
    "model_name": "default",
    "litellm_params": {
        "model": FLASH,
    }
}]
litellm.model = "default"

def parse_xml(xml_string: str) -> Dict[str, Any]:
    try:
        root: ET.Element = ET.fromstring(xml_string)
        return _parse_element(root)
    except ET.ParseError as e:
        print(f"Invalid XML: {e}")
        return {}


def _parse_element(element: ET.Element) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for child in element:
        child_data: Any
        if len(child) > 0:  # Has nested elements
            child_data = _parse_element(child)
        elif child.text:
            child_data = child.text.strip()
        else:
            child_data = None

        if child.tag in result:
            if not isinstance(result[child.tag], list):
                result[child.tag] = [result[child.tag]]
            if isinstance(result[child.tag], list):
                 result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data
    return result

def litellm_completion(prompt: str, model: str = FLASH) -> str:
    messages: List[Dict[str, str]] = [{"role": "user", "content": prompt}]
    try:
        response = litellm.completion(model=model, messages=messages)
        if response and response.choices and response.choices[0].message:
            return response.choices[0].message.content or ""
        return ""
    except litellm.LiteLLMError as e:
        print(f"LiteLLMError during litellm completion: {type(e).__name__} - {e}")
        return ""
    except Exception as e:
        print(f"General error during litellm completion: {type(e).__name__} - {e}")
        return ""


def litellm_streaming(prompt: str, model: str = FLASH, max_tokens: Optional[int] = None) -> Generator[str, None, None]:
    """Uses the litellm library to stream a completion.
    """
    messages: List[Dict[str, str]] = [{"role": "user", "content": prompt}]
    kwargs: Dict[str, Any] = {"model": model, "messages": messages, "stream": True}
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens
    try:
        response: Any = litellm.completion(**kwargs)
        if isinstance(response, dict):  # Handle non-streaming response
            if 'choices' in response and len(response['choices']) > 0 and 'message' in response['choices'][0]:
                yield response['choices'][0]['message']['content'] or ""
            else:
                print(f"Unexpected non-streaming response format: {response}")
                yield ""
        else:  # Handle streaming response
            for chunk in response:
                if (
                    chunk.get('choices')
                    and len(chunk['choices']) > 0
                    and chunk['choices'][0].get('delta')
                    and chunk['choices'][0]['delta'].get('content')
                ):
                    content: str = chunk['choices'][0]['delta']['content']
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
    return "test_output_var"


def test_env_1(input_str: str) -> int:
    if 'aaa' in input_str:
        return 3
    return 4


class Agent:
    def __init__(self, model: str = FLASH) -> None:
        self.model: str = model
        self.memory: str = ""
        self.last_completion: str = ""

    def reply(self, prompt: str) -> str:
        self.last_completion = litellm_completion(prompt, self.model)
        return self.last_completion

    def _parse_xml(self, xml_string: str) -> Dict[str, Any]:
        return parse_xml(xml_string)

    def _update_memory(self, search: str, replace: str) -> None:
        if search and search in self.memory:
            self.memory = self.memory.replace(search, replace)
        else:
            self.memory += f"\n{replace}"


class AgentAssert:
    def __init__(self, model: str = FLASH) -> None:
        self.agent: Agent = Agent(model=model)

    def __call__(self, prompt: str) -> bool:
        response: str = self.agent.reply(prompt)
        parsed: Dict[str, Any] = self.agent._parse_xml(response)
        if 'message' in parsed:
            message: str = parsed['message']
            if "match specifications" in message:
                return False
        return True

    def _parse_xml(self, xml_string: str) -> bool:
        parsed: Dict[str, Any] = parse_xml(xml_string)
        if 'bool' in parsed:
            bool_value: str = parsed['bool']
            return bool_value.lower() == 'true'
        return False
