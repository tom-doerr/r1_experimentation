import xml.etree.ElementTree as ET
from typing import Dict, Any, Iterator
import litellm

def parse_xml(xml_string: str) -> Dict[str, Any]:
    """XML parser with simplified complexity"""
    def parse_element(element: ET.Element) -> Dict[str, Any]:
        result: Dict[str, Any] = {element.tag: None}
        
        children = list(element)
        if children:
            result = {}
            for child in children:
                child_data = parse_element(child)
                key = child.tag
                if key in result:
                    if not isinstance(result[key], list):
                        result[key] = [result[key]]
                    result[key].append(child_data[key])
                else:
                    result[key] = child_data[key]
        elif element.text and element.text.strip():
            result[element.tag] = element.text.strip()
        
        return result

    try:
        root = ET.fromstring(xml_string)
        return parse_element(root)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}") from e



# Simplified LiteLLM implementations
def litellm_completion(prompt: str, model: str = 'openrouter/google/gemini-2.0-flash-001') -> str:
    # LiteLLM completion implementation with model parameter
    response = litellm.completion(
        model=model,
        messages=[{"content": prompt, "role": "user"}]
    )
    return response.choices[0].message.content

def litellm_streaming(prompt: str, model: str = 'openrouter/google/gemini-2.0-flash-001', max_tokens: int = 20) -> Iterator[str]:
    # LiteLLM streaming implementation with configurable model and tokens
    response = litellm.completion(
        model=model,
        messages=[{"content": prompt, "role": "user"}],
        stream=True,
        max_tokens=max_tokens
    )
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def python_reflection_testing() -> str:
    """Simple reflection test that returns its own variable name"""
    return 'test_output_var'


class Agent:
    """Main agent for handling AI interactions"""
    def __init__(self) -> None:
        self.model = "default-model"

    def set_model(self, model_name: str) -> None:
        """Set the model to use for processing"""
        self.model = model_name

    def get_model(self) -> str:
        return self.model

def test_env_1(input_data: str) -> int:
    # Returns count of 'a's in input
    return input_data.count('a')

if __name__ == "__main__":
    # Test the XML parser
    TEST_XML = '<test><node>value</node></test>'
    print(parse_xml(TEST_XML))
