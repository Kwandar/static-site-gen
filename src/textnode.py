from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    PLAIN = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode:
    def __init__(self, text="", text_type=TextType.PLAIN, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    for text_type in TextType:
        if text_node.text_type == text_type:
            if text_type == TextType.PLAIN:
                return LeafNode(None, text_node.text)
            elif text_type == TextType.BOLD:
                return LeafNode("b", text_node.text)
            elif text_type == TextType.ITALIC:
                return LeafNode("i", text_node.text)
            elif text_type == TextType.CODE:
                return LeafNode("code", text_node.text)
            elif text_type == TextType.LINK:
                return LeafNode("a", text_node.text, props={"href": text_node.url})
            elif text_type == TextType.IMAGE:
                return LeafNode("img", None, props={"src": text_node.url, "alt": text_node.text})
    raise Exception(f"Unsupported text type: {text_node.text_type}")