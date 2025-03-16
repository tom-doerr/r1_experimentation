import xml.etree.ElementTree as ET

def parse_xml(xml_string: str) -> dict:
    # Parse XML string and return flattened dict of text content
    root = ET.fromstring(xml_string)
    result = {}
    
    def parse_element(element):
        # Recursively parse elements, flattening the structure
        if len(element) == 0:  # Leaf node
            return element.text
        return {child.tag: parse_element(child) for child in element}
    
    # Start parsing from root's children
    for child in root:
        result[child.tag] = parse_element(child)
    return result

if __name__ == "__main__":
    # Test the XML parser
    test_xml = '<test><node>value</node></test>'
    print(parse_xml(test_xml))
