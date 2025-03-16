import xml.etree.ElementTree as ET

def parse_xml(xml_string: str) -> dict:
    root = ET.fromstring(xml_string)
    result = {}
    
    def parse_element(element):
        # Handle text content even if element has children
        text = element.text.strip() if element.text else None
        if text:
            return text
        
        # Recursively parse children
        return {child.tag: parse_element(child) for child in element}
    
    # Parse root element directly
    return {root.tag: parse_element(root)}

if __name__ == "__main__":
    # Test the XML parser
    test_xml = '<test><node>value</node></test>'
    print(parse_xml(test_xml))
