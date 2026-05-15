from textnode import TextNode, TextType
import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 1,
    HEADING = 2,
    CODE = 3,
    QUOTE = 4,
    UNORDERED_LIST = 5,
    ORDERED_LIST = 6


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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if not images:
                new_nodes.append(node)
            else:
                split_text = re.split(r"!\[[^\[\]]*\]\([^\(\)]*\)", node.text)
                for i, text in enumerate(split_text):
                    if text:
                        new_nodes.append(TextNode(text, TextType.PLAIN))
                    if i < len(images):
                        alt_text, url = images[i]
                        new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            if not links:
                new_nodes.append(node)
            else:
                split_text = re.split(r"(?<!!)\[[^\[\]]*\]\([^\(\)]*\)", node.text)
                for i, text in enumerate(split_text):
                    if text:
                        new_nodes.append(TextNode(text, TextType.PLAIN))
                    if i < len(links):
                        link_text, url = links[i]
                        new_nodes.append(TextNode(link_text, TextType.LINK, url))
    return new_nodes

def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    # now we split text with delimiter for bold, italic, and code
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = [node for node in nodes if node.text]  # remove empty nodes
    return nodes

def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")  # split by double newlines to get blocks
    blocks = []
    for line in lines:
        if line.strip() == "":
            continue
        blocks.append(line.strip())
    return blocks

def block_to_block_type(block):
    if block.startswith("# "):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif re.match(r"^\d+\. ", block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
