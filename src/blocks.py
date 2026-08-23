from enum import Enum

from functions import text_to_textnodes
from htmlnode import HTMLNode, ParentNode
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    new_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block:
            new_blocks.append(block)
    return new_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        for i in range(len(lines)):
            if not lines[i].startswith(f"{i + 1}. "):
                            return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def block_to_htmlnode(block):
    blocktype = block_to_block_type(block)
    if blocktype == BlockType.HEADING:
        heading = block.split(" ", 1)
        level = len(heading[0])
        tag = f"h{level}"
        children = text_to_children(heading[1])
        return ParentNode(tag, children)

    if blocktype == BlockType.PARAGRAPH:
        new_lines = []
        lines = block.split("\n")
        for line in lines:
            new_lines.append(line.strip(" "))
        lines = " ".join(new_lines)
        children = text_to_children(lines)
        return ParentNode("p", children)

    if blocktype == BlockType.QUOTE:
        new_lines = []
        lines = block.split("\n")
        for line in lines:
            if line.startswith("> "):
                new_lines.append(line[2:])
            else:
                new_lines.append(line[1:])
        lines = " ".join(new_lines)
        children = text_to_children(lines)
        return ParentNode("blockquote", children)

    if blocktype == BlockType.CODE:
        text = block[3:-3].lstrip("\n")
        text_node = TextNode(text, TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        return ParentNode("pre", [ParentNode("code", [html_node])])

    if blocktype == BlockType.UNORDERED_LIST:
        children = []
        lines = block.split("\n")
        for line in lines:
            line = line[2:]
            children.append(ParentNode("li", text_to_children(line)))
        return ParentNode("ul", children)

    if blocktype == BlockType.ORDERED_LIST:
        children = []
        lines = block.split("\n")
        for line in lines:
            parts = line.split(". ", 1)
            children.append(ParentNode("li", text_to_children(parts[1])))
        return ParentNode("ol", children)



def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        html_node = block_to_htmlnode(block)
        html_nodes.append(html_node)
    return ParentNode("div", html_nodes)
