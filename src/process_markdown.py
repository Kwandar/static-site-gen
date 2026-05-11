from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise ValueError(f"Invalid markdown syntax: unmatched delimiter '{delimiter}'")
            for i, text in enumerate(split_text):
                if i % 2 == 1 or text:
                    if i % 2 == 0:
                        new_nodes.append(TextNode(text, TextType.PLAIN))
                    else:
                        new_nodes.append(TextNode(text, text_type))
    return new_nodes
    
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)