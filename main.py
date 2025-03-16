import xml.etree.ElementTree as ET
from typing import Dict, Any, Generator

def parse_xml(xml_string: str) -> Dict[str, Any]:
    def parse_element(element: ET.Element) -> Dict[str, Any]:
        result = {}
        for child in element:
            # Handle both text and nested elements
            if len(child) == 0:  # No nested elements
                result[child.tag] = child.text.strip() if child.text else None
            else:
                result[child.tag] = parse_element(child)
        return result

    root = ET.fromstring(xml_string)
    return parse_element(root)

def litellm_completion(prompt: str, model: str = '') -> str:
    # Simple mock implementation for testing
    return f"Mock response to: {prompt}"

def litellm_streaming(prompt: str, model: str = '') -> Generator[str, None, None]:
    # Simple mock streaming implementation
    yield f"Streaming response to: {prompt}"

class Agent:
    pass

if __name__ == "__main__":
    # Test the XML parser
    TEST_XML = '<test><node>value</node></test>'
    print(parse_xml(TEST_XML))
