import xml.etree.ElementTree as ET
from typing import Dict, Any, Iterator, Optional

def parse_xml(xml_string: str) -> Dict[str, Any]:
    """XML parser with nested structure support"""
    try:
        root = ET.fromstring(xml_string)
        return parse_element(root)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}") from e

def parse_element(element: ET.Element) -> Dict[str, Any]:
    result: Dict[str, Any] = {element.tag: {}}

    if element.text and element.text.strip():
        result[element.tag]['value'] = element.text.strip()

    for child in element:
        child_data = parse_element(child)
        if child.tag in result[element.tag]:
            if isinstance(result[element.tag][child.tag], list):
                result[element.tag][child.tag].append(child_data[child.tag])
            else:
                result[element.tag][child.tag] = [result[element.tag][child.tag], child_data[child.tag]]
        else:
            result[element.tag][child.tag] = child_data[child.tag]

    return result
