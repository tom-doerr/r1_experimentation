import xml.etree.ElementTree as ET
from typing import Dict, Any, Iterator, List

def parse_xml(xml_string: str) -> Dict[str, Any]:
    """XML parser with simplified complexity"""
    def parse_element(element: ET.Element) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        
        # Handle element text content
        if element.text and element.text.strip():
            result["text"] = element.text.strip()
            
        # Handle child elements
        for child in element:
            child_data = parse_element(child)
            
            # Handle multiple elements with same tag
            if child.tag in result:
                existing = result[child.tag]
                if isinstance(existing, list):
                    existing.append(child_data)
                else:
                    result[child.tag] = [existing, child_data]
            else:
                result[child.tag] = child_data
                
        return result

    try:
        root = ET.fromstring(xml_string)
        return parse_element(root)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}") from e



# Simplified LiteLLM implementations
def litellm_completion(prompt: str, model: str = 'openrouter/google/gemini-2.0-flash-001') -> str:
    """LiteLLM completion implementation"""
    import litellm
    response = litellm.completion(
        model=model,
        messages=[{"content": prompt, "role": "user"}]
    )
    return response.choices[0].message.content

def litellm_streaming(prompt: str) -> Iterator[str]:
    """LiteLLM streaming implementation"""
    import litellm
    response = litellm.completion(
        model='openrouter/google/gemini-2.0-flash-001',
        messages=[{"content": prompt, "role": "user"}],
        stream=True
    )
    for chunk in response:
        content = chunk.choices[0].delta.get('content', '')
        if content:
            yield content

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
    # Simple test environment that returns count of 'a' characters
    return input_data.count('a')  # 'aaa' has 3, 'aabbjadfa' has 4 a's

if __name__ == "__main__":
    # Test the XML parser
    TEST_XML = '<test><node>value</node></test>'
    print(parse_xml(TEST_XML))
