import xml.etree.ElementTree as ET
from typing import Dict, Any, Iterator, Optional
import litellm

def parse_xml(xml_string: str) -> Dict[str, Any]:
    """XML parser with nested structure support"""
    def parse_element(element: ET.Element) -> Dict[str, Any]:
        result = {}
        result[element.tag] = {}  # Initialize the tag

        if element.text and element.text.strip():
            result[element.tag]['value'] = element.text.strip()

        for child in element:
            child_data = parse_element(child)
            if child.tag in result[element.tag]:  # If the tag already exists
                if isinstance(result[element.tag][child.tag], list):  # If it's a list, append
                    result[element.tag][child.tag].append(child_data[child.tag])  # Append new data
                else:
                    result[element.tag][child.tag] = [result[element.tag][child.tag], child_data[child.tag]]  # Convert to list and append
            else:
                result[element.tag][child.tag] = child_data[child.tag]  # Add the new tag

        return result

    try:
        root = ET.fromstring(xml_string)
        return parse_element(root)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}") from e
