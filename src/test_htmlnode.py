import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            value="Visit Boot.dev",
            children=None,
            props={"href": "https://www.boot.dev", "target": "_blank"}
        )
        output = ' href="https://www.boot.dev" target="_blank"'
        self.assertEqual(node.props_to_html(), output)

    def test_props_to_html_none(self):
        node = HTMLNode(
            tag="a",
            value="Visit Boot.dev",
            children=None
        )
        output = ""
        self.assertEqual(node.props_to_html(), output)

    def test_values(self):
        node = HTMLNode(
            tag="a",
            value="Visit Boot.dev",
        )
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

if __name__ == "__main__":
    unittest.main()
