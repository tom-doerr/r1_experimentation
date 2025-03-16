import xml.etree.ElementTree as ET

def parse_xml(xml_string: str) -> dict:
    # Parse XML string and extract text content from elements
    root = ET.fromstring(xml_string)
    result = {}
    
    # Recursively parse all elements
    def parse_element(element, parent_dict):
        if len(element) == 0:  # Leaf node
            parent_dict[element.tag] = element.text
        else:  # Branch node
            new_dict = {}
            parent_dict[element.tag] = new_dict
            for child in element:
                parse_element(child, new_dict)
    
    parse_element(root, result)
    return result

if __name__ == "__main__":
    # Test the XML parser
    test_xml = '<test><node>value</node></test>'
    print(parse_xml(test_xml))
