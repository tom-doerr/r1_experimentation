import xml.etree.ElementTree as ET
from typing import Dict, Any

def parse_xml(xml_string: str) -> Dict[str, Any]:
    """XML parser with nested structure support"""
    try:
        root = ET.fromstring(xml_string)
        return _parse_element(root)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}") from e

def _parse_element(element: ET.Element) -> Dict[str, Any]:
    result: Dict[str, Any] = {}

    if element.text and element.text.strip():
        result['value'] = element.text.strip()

    for child in element:
        child_data = _parse_element(child)
        if child.tag in result:
            if isinstance(result[child.tag], list):
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data

    return {element.tag: result}
