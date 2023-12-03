from xml.dom.minidom import Document, parse, parseString
import codecs

# Define the encoding to be used
enc = "utf_8"

def _encode(v):
    # In Python 3, all strings are unicode by default.
    # If you need to encode strings for a specific reason, you can use v.encode(enc)
    return v

class XMLElement:
    def __init__(self, doc, el):
        self.doc = doc
        self.el = el

    def __getitem__(self, name):
        a = self.el.getAttributeNode(name)
        if a:
            return _encode(a.value)
        return None

    def __setitem__(self, name, value):
        self.el.setAttribute(name, _encode(value))

    def __delitem__(self, name):
        self.el.removeAttribute(name)

    def __str__(self):
        return _encode(self.doc.toprettyxml())

    def toString(self):
        return self.doc.toxml()

    def _inst(self, el):
        return XMLElement(self.doc, el)

    def get(self, name, default=None):
        a = self.el.getAttributeNode(name)
        if a:
            return _encode(a.value)
        return _encode(default)

    def add(self, tag, **kwargs):
        el = self.doc.createElement(tag)
        for k, v in kwargs.items():
            el.setAttribute(k, _encode(str(v)))
        return self._inst(self.el.appendChild(el))

    def addText(self, data):
        return self._inst(self.el.appendChild(self.doc.createTextNode(_encode(data))))

    def addComment(self, data):
        return self._inst(self.el.appendChild(self.doc.createComment(data)))

    def getText(self, sep=" "):
        rc = []
        for node in self.el.childNodes:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return _encode(sep.join(rc))

    def getAll(self, tag):
        return list(map(self._inst, self.el.getElementsByTagName(tag)))

class XMLDocument(XMLElement):
    def __init__(self, tag=None, **kwargs):
        self.doc  = Document()
        XMLElement.__init__(self, self.doc, self.doc)
        if tag:
            self.el = self.add(tag, **kwargs).el

    def writexml(self, writer, indent='', addindent='', newl=''):
        # The writexml method now takes a writer object instead of just a file path.
        self.doc.writexml(writer, indent, addindent, newl)

    def parse(self, d):
        self.doc = self.el = parse(d)
        return self

    def parseString(self, d):
        self.doc = self.el = parseString(_encode(d))
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

    # Output the document to a file
    with codecs.open('test.xml', 'w', 'utf_8') as f:
        doc.writexml(f)

    # If you need to pretty print to console
    print(doc)
