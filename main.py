import xml.etree.ElementTree as ET
from typing import Dict, Any, Generator

def parse_xml(xml_string: str) -> Dict[str, Any]:
    root = ET.fromstring(xml_string)
    result = {}

    def parse_element(element: ET.Element) -> Any:
        # Return text content if no children
        if len(element) == 0:
            return element.text.strip() if element.text else None
            
        # Parse children into dict
        child_data = {}
        for child in element:
            child_data[child.tag] = parse_element(child)
        return child_data

    # Flatten root structure
    return parse_element(root)

def litellm_completion(prompt: str) -> str:
    # Simple mock implementation for testing
    return f"Mock response to: {prompt}"

def litellm_streaming(prompt: str) -> Generator[str, None, None]:
    # Simple mock streaming implementation
    yield f"Streaming response to: {prompt}"

if __name__ == "__main__":
    # Test the XML parser
    test_xml = '<test><node>value</node></test>'
    print(parse_xml(test_xml))
