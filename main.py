import xml.etree.ElementTree as ET
from typing import Dict, Any, Generator

def parse_xml(xml_string: str) -> Dict[str, Any]:
    root = ET.fromstring(xml_string)
    
    # Extract direct children of root element
    result = {}
    for child in root:
        # Get text content if no nested elements
        if len(child) == 0:
            result[child.tag] = child.text.strip() if child.text else None
        else:
            # Handle nested elements recursively
            result[child.tag] = parse_xml(ET.tostring(child).decode())
            
    return result

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
