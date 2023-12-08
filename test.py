from xml.dom.minidom import Document

def create_pretty_xml():
    # Create a new XML document and an element
    doc = Document()
    root_element = doc.createElement('root')
    doc.appendChild(root_element)

    # Add some child elements
    for i in range(3):
        child = doc.createElement('child')
        child.setAttribute('id', str(i))
        root_element.appendChild(child)

    # Generate a pretty-printed XML string
    pretty_xml_string = doc.toprettyxml(indent="    ")

    print(doc.encoding)

    return pretty_xml_string

def save_to_file(filename, xml_content):
    # Save the pretty-printed XML to a file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(xml_content)

# Create pretty XML
pretty_xml = create_pretty_xml()
print(pretty_xml)

# Save to 'test.xml'
save_to_file('test.xml', pretty_xml)

print("XML saved to test.xml")
