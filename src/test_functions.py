import unittest
from textnode import TextNode, TextType
from functions import (
    split_nodes_delimiter, extract_markdown_images,
    split_nodes_image, split_nodes_link,
    text_to_textnodes)
from blocks import (
    markdown_to_blocks, BlockType,
    block_to_block_type, markdown_to_html_node)
from extract_title import extract_title

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_some_descriptive_name(self):
        # Setup: create your input node(s)
        node = TextNode("help **i need** help coding", TextType.TEXT)

        # Action: call your function
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        # Assertion: check the result
        self.assertEqual(new_nodes, [
            TextNode("help ", TextType.TEXT),
            TextNode("i need", TextType.BOLD),
            TextNode(" help coding", TextType.TEXT)
        ])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, expected)

    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_block_to_block_type(self):
        # 1. Heading test
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        # 2. Code test
        block = "```\ncode goes here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        # 3. Quote test
        block = "> quote line 1\n> quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

         # 4. Unordered list test
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        # 5. Ordered list test
        block = "1. first item\n2. second item\n3. third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        # 6. Paragraph test
        block = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_extract_title(self):
        md = """
what are you doing
# Hello
blah bah
        """
        title = extract_title(md)
        self.assertEqual(title, "Hello")
