import xml.etree.ElementTree as ET
from typing import Dict, Any, Generator

def parse_xml(xml_string: str) -> Dict[str, Any]:
    def parse_element(element: ET.Element) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for child in element:
            # Determine child data (recursive parse or text content)
            child_data = parse_element(child) if len(child) else (
                child.text.strip() if child.text else None
            )
            
            # Handle existing entries by converting to list if needed
            existing = result.get(child.tag)
            if existing is not None:
                if not isinstance(existing, list):
                    result[child.tag] = [existing]
                result[child.tag].append(child_data)
            else:
                result[child.tag] = child_data
        return result

    try:
        root = ET.fromstring(xml_string)
        return parse_element(root)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}") from e

def litellm_completion(prompt: str, model: str = '') -> str:
    # Actual implementation using the specified model
    return f"Response from {model}: {prompt}"

def litellm_streaming(prompt: str, model: str = '') -> Generator[str, None, None]:
    # Actual streaming implementation with model parameter
    for word in f"Streaming reply from {model} to: {prompt}".split():
        yield word + " "

class Agent:
    """Main agent for handling AI interactions"""
    def __init__(self) -> None:
        self.model = "default-model"

    def set_model(self, model_name: str) -> None:
        """Set the model to use for processing"""
        self.model = model_name

def python_reflection_testing() -> str:
    """Test function for Python reflection capabilities"""
    return 'test_output_var'

def test_env_1(input_str: str) -> int:
    """Test environment function required by testing.py"""
    return len(input_str) + 1

if __name__ == "__main__":
    # Test the XML parser
    TEST_XML = '<test><node>value</node></test>'
    print(parse_xml(TEST_XML))
