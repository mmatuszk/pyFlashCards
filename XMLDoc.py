from xml.dom.minidom import Document, parse, parseString
import codecs

class XMLElement:
    def __init__(self, doc, el):
        self.doc = doc
        self.el = el

    def __getitem__(self, name):
        a = self.el.getAttributeNode(name)
        if a:
            return a.value
        return None

    def __setitem__(self, name, value):
        self.el.setAttribute(name, value)

    def __delitem__(self, name):
        self.el.removeAttribute(name)

    def __str__(self):
        return self.doc.toprettyxml()

    def toString(self):
        return self.doc.toxml()

    def _inst(self, el):
        return XMLElement(self.doc, el)

    def get(self, name, default=None):
        a = self.el.getAttributeNode(name)
        if a:
            return a.value
        return default

    def add(self, tag, **kwargs):
        el = self.doc.createElement(tag)
        for k, v in kwargs.items():
            el.setAttribute(k, str(v))
        return self._inst(self.el.appendChild(el))

    def addText(self, data):
        return self._inst(self.el.appendChild(self.doc.createTextNode(data)))

    def addComment(self, data):
        return self._inst(self.el.appendChild(self.doc.createComment(data)))

    def getText(self, sep=" "):
        rc = []
        for node in self.el.childNodes:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return sep.join(rc)

    def getAll(self, tag):
        return list(map(self._inst, self.el.getElementsByTagName(tag)))

class XMLDocument(XMLElement):
    def __init__(self, tag=None, **kwargs):
        self.doc  = Document()
        XMLElement.__init__(self, self.doc, self.doc)
        if tag:
            self.el = self.add(tag, **kwargs).el

    # def writexml(self, writer, indent='', addindent='', newl=''):
        #  The writexml method now takes a writer object instead of just a file path.
        #self.doc.writexml(writer, indent, addindent, newl)
        #formatted_xml = self.doc.toprettyxml(indent, newl)

    def writexml(self, writer, indent='    ', newl='\n'):
        try:
            formatted_xml = self.doc.toprettyxml(indent, newl)
            writer.write(formatted_xml)
            print("XML document written successfully.")
        except Exception as e:
            print("Error while writing XML document:", e)

    def parse(self, d):
        self.doc = self.el = parse(d)
        return self

    def parseString(self, d):
        self.doc = self.el = parseString(d)
        return self

# Below is an example of how you might use these classes.
if __name__ == "__main__":
    # Create a new XMLDocument with a root tag of 'data'
    doc = XMLDocument("data")

    # Add chapters
    cl = doc.add('chapter_list')
    cl.add('chapter').addText('Chapter 1')
    cl.add('chapter').addText('Chapter 2')

    # Add cards
    cards = doc.add('cards')
    c = cards.add('card')
    c.add('front').addText('front 1')
    c.add('back').addText('back 1')
    c.add('chapter').addText('Chapter 1')
    c.add('box').addText('1')

    #pretty_xml_string = doc.toprettyxml(indent="    ")
    #print(pretty_xml_string)

    # Output the document to a file
    with codecs.open('test.xml', 'w', 'utf_8') as f:
        doc.writexml(f)

    # If you need to pretty print to console
    print(doc)
