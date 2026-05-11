import unittest
from process_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiters(self):
        nodes = [TextNode("hello world", TextType.PLAIN)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("hello world", TextType.PLAIN)]
        self.assertEqual(result, expected)

    def test_single_bold(self):
        nodes = [TextNode("hello **world**", TextType.PLAIN)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("hello ", TextType.PLAIN), TextNode("world", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_multiple_bold(self):
        nodes = [TextNode("hello **world** and **more**", TextType.PLAIN)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("hello ", TextType.PLAIN),
            TextNode("world", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("more", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_italic(self):
        nodes = [TextNode("hello *world*", TextType.PLAIN)]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected = [TextNode("hello ", TextType.PLAIN), TextNode("world", TextType.ITALIC)]
        self.assertEqual(result, expected)

    def test_code(self):
        nodes = [TextNode("hello `code`", TextType.PLAIN)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [TextNode("hello ", TextType.PLAIN), TextNode("code", TextType.CODE)]
        self.assertEqual(result, expected)

    def test_missing_closing_delimiter(self):
        nodes = [TextNode("hello **world", TextType.PLAIN)]
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertIn("unmatched delimiter", str(cm.exception))

    def test_extra_closing_delimiter(self):
        nodes = [TextNode("hello **world** **", TextType.PLAIN)]
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertIn("unmatched delimiter", str(cm.exception))

    def test_empty_between_delimiters(self):
        nodes = [TextNode("****", TextType.PLAIN)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_non_plain_node_unchanged(self):
        nodes = [TextNode("**world**", TextType.BOLD)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("**world**", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_mixed_nodes(self):
        nodes = [
            TextNode("plain text", TextType.PLAIN),
            TextNode("**bold**", TextType.BOLD),
            TextNode("more **italic** here", TextType.PLAIN)
        ]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("plain text", TextType.PLAIN),
            TextNode("**bold**", TextType.BOLD),
            TextNode("more ", TextType.PLAIN),
            TextNode("italic", TextType.BOLD),
            TextNode(" here", TextType.PLAIN)
        ]
        self.assertEqual(result, expected)

    def test_start_with_delimiter(self):
        nodes = [TextNode("**bold** text", TextType.PLAIN)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [TextNode("bold", TextType.BOLD), TextNode(" text", TextType.PLAIN)]
        self.assertEqual(result, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        text = "Here is a link: [example](http://example.com)"
        result = extract_markdown_links(text)
        expected = [("example", "http://example.com")]
        self.assertEqual(result, expected)

    def test_extract_multiple_images_and_links(self):
        text = "Image: ![alt](http://example.com/image.jpg) and Link: [example](http://example.com)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertEqual(images, [("alt", "http://example.com/image.jpg")])
        self.assertEqual(links, [("example", "http://example.com")])

    def test_extract_no_images_or_links(self):
        text = "No images or links here."
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertEqual(images, [])
        self.assertEqual(links, [])
    
    def test_extract_malformed_markdown(self):
        text = "Malformed image ![alt](http://example.com/image.jpg and malformed link [example(http://example.com)"
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertEqual(images, [])
        self.assertEqual(links, [])

if __name__ == "__main__":
    unittest.main()