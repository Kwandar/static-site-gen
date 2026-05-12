import unittest
from process_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_text_nodes
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

    def test_split_images(self):
        nodes = [TextNode("This is an image: ![alt](http://example.com/image.jpg)", TextType.PLAIN)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("This is an image: ", TextType.PLAIN),
            TextNode("alt", TextType.IMAGE, "http://example.com/image.jpg")
        ]
        self.assertEqual(result, expected)
    
    def test_split_links(self):
        nodes = [TextNode("This is a link: [example](http://example.com)", TextType.PLAIN)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("This is a link: ", TextType.PLAIN),
            TextNode("example", TextType.LINK, "http://example.com")
        ]
        self.assertEqual(result, expected)

    def test_split_malformed_markdown(self):
        nodes = [TextNode("Malformed image ![alt](http://example.com/image.jpg and malformed link [example(http://example.com)", TextType.PLAIN)]
        result_images = split_nodes_image(nodes)
        result_links = split_nodes_link(nodes)
        expected = [TextNode("Malformed image ![alt](http://example.com/image.jpg and malformed link [example(http://example.com)", TextType.PLAIN)]
        self.assertEqual(result_images, expected)
        self.assertEqual(result_links, expected)

    def test_split_multiple_images_and_links(self):
        nodes = [TextNode("Image: ![alt](http://example.com/image.jpg) and Link: [example](http://example.com)", TextType.PLAIN)]
        result_images = split_nodes_image(nodes)
        result_links = split_nodes_link(result_images)
        expected = [
            TextNode("Image: ", TextType.PLAIN),
            TextNode("alt", TextType.IMAGE, "http://example.com/image.jpg"),
            TextNode(" and Link: ", TextType.PLAIN),
            TextNode("example", TextType.LINK, "http://example.com")
        ]
        self.assertEqual(result_links, expected)

    def test_non_plain_node_unchanged(self):
        nodes = [TextNode("![alt](http://example.com/image.jpg)", TextType.IMAGE, "http://example.com/image.jpg")]
        result = split_nodes_image(nodes)
        expected = [TextNode("![alt](http://example.com/image.jpg)", TextType.IMAGE, "http://example.com/image.jpg")]
        self.assertEqual(result, expected)

    def test_multiple_types_of_markdown(self):
        nodes = [TextNode("**bold** and *italic* and `code`", TextType.PLAIN)]
        result_bold = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        result_italic = split_nodes_delimiter(result_bold, "*", TextType.ITALIC)
        result_code = split_nodes_delimiter(result_italic, "`", TextType.CODE)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.PLAIN),
            TextNode("code", TextType.CODE)
        ]
        self.assertEqual(result_code, expected)
    
    def test_multiple_markdown_with_images_and_links(self):
        nodes = [TextNode("**bold** and ![alt](http://example.com/image.jpg) and [example](http://example.com)", TextType.PLAIN)]
        result_bold = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        result_images = split_nodes_image(result_bold)
        result_links = split_nodes_link(result_images)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.PLAIN),
            TextNode("alt", TextType.IMAGE, "http://example.com/image.jpg"),
            TextNode(" and ", TextType.PLAIN),
            TextNode("example", TextType.LINK, "http://example.com")
        ]
        self.assertEqual(result_links, expected)
    
    def test_text_to_text_nodes(self):
        text = "This is **bold** text with an ![image](http://example.com/image.jpg) and a [link](http://example.com)."
        result = text_to_text_nodes(text)
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "http://example.com/image.jpg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(".", TextType.PLAIN)
        ]
        self.assertEqual(result, expected)

    def test_text_to_text_nodes_with_italic_and_code(self):
        text = "This is *italic* and `code` with an ![image](http://example.com/image.jpg) and a [link](http://example.com)."
        result = text_to_text_nodes(text)
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("image", TextType.IMAGE, "http://example.com/image.jpg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(".", TextType.PLAIN)
        ]
        self.assertEqual(result, expected)

    def test_text_to_text_nodes_with_malformed_markdown(self):
        text = "Malformed image ![alt](http://example.com/image.jpg and malformed link [example(http://example.com)"
        result = text_to_text_nodes(text)
        expected = [TextNode("Malformed image ![alt](http://example.com/image.jpg and malformed link [example(http://example.com)", TextType.PLAIN)]
        self.assertEqual(result, expected)

    def test_text_to_text_nodes_with_empty_markdown(self):
        text = "This is **** and ****"
        result = text_to_text_nodes(text)
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode(" and ", TextType.PLAIN)
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnodes_with_all_different_text_types(self):
        text = "**bold** *italic* `code` ![alt](http://example.com/image.jpg) [link](http://example.com)"
        result = text_to_text_nodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.PLAIN),
            TextNode("alt", TextType.IMAGE, "http://example.com/image.jpg"),
            TextNode(" ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "http://example.com")
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()