from html.parser import HTMLParser
from html.entities import name2codepoint
import string

class HTMLStrippingParser(HTMLParser):

    # These are the HTML tags that we will leave intact
    valid_tags = ('b', 'a', 'i', 'br', 'p')

    def __init__(self):
        super().__init__()
        self.result = ""
        self.endTagList = [] 
        
    def handle_data(self, data):
        if data:
            self.result += data

    def handle_charref(self, name):
        try:
            self.result += chr(int(name))
        except ValueError:
            self.result += "&#{};".format(name)
        
    def handle_entityref(self, name):
        if name in name2codepoint: 
            self.result += chr(name2codepoint[name])
        else:
            # In case of unknown entity, keep it as it is
            self.result += "&{};".format(name)
    
    def handle_starttag(self, tag, attrs):
        """ Delete all tags except for legal ones """
        if tag in self.valid_tags:       
            self.result += '<' + tag
            for k, v in attrs:
                if k.lower()[:2] != 'on' and v.lower()[:10] != 'javascript':
                    self.result += ' {}="{}"'.format(k, v)
            endTag = '</{}>'.format(tag)
            self.endTagList.insert(0, endTag)    
            self.result += '>'
                
    def handle_endtag(self, tag):
        if tag in self.valid_tags:
            self.result += "</{}>".format(tag)
            remTag = '</{}>'.format(tag)
            self.endTagList.remove(remTag)

    def cleanup(self):
        """ Append missing closing tags """
        for tag in self.endTagList:
            self.result += tag    

def strip_tags(html):
    """ Strip illegal HTML tags from string s """
    parser = HTMLStrippingParser()
    parser.feed(html)
    parser.close()
    parser.cleanup()
    return parser.result

if __name__ == '__main__':
    my_str = "<b>Hello World</b>\n<i>Marcin</i>"

    print(strip_tags(my_str))
