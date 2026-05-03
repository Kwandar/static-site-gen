import unittest

from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"class": "my-class", "id": "my-id"})
        self.assertEqual(node.props_to_html(), ' class="my-class" id="my-id"')

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')
    
    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello", children=[], props={"class": "my-class"})
        expected_repr = "HTMLNode(tag=div, value=Hello, children=[], props={'class': 'my-class'})"
        self.assertEqual(repr(node), expected_repr)

    def test_props_to_html2(self):
        node = HTMLNode(props={"data-test": "value", "aria-label": "label"})
        self.assertEqual(node.props_to_html(), ' data-test="value" aria-label="label"')


if __name__ == "__main__":
    unittest.main()