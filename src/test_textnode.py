import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, TextNode("This is a text node", TextType.ITALIC))
        self.assertNotEqual(node, TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev"))
        self.assertNotEqual(node, TextNode("This is a different text node", TextType.BOLD))

    def test_plain_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)
    
    def test_bold_text(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.props, None)
    
    def test_italic_text(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.props, None)

    def test_code_text(self):
        node = TextNode("This is code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code text")
        self.assertEqual(html_node.props, None)

    def test_link_text(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image_text(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev/image.png", "alt": "This is an image"})

    def test_unsupported_text_type(self):
        node = TextNode("This is an unsupported text type", 58)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
        



if __name__ == "__main__":
    unittest.main()