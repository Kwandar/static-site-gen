import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello, world!")
        self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

    def test_leaf_repr(self):
        node = LeafNode("div", "Hello, world!", props={"class": "my-class"})
        expected_repr = "LeafNode(tag=div, value=Hello, world!, props={'class': 'my-class'})"
        self.assertEqual(repr(node), expected_repr)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # ParentNode Error-Proofing Tests
    
    def test_parent_node_no_tag(self):
        """ParentNode should raise ValueError when tag is None"""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_node_none_children(self):
        """ParentNode should raise error when children is None"""
        parent_node = ParentNode("div", None)
        with self.assertRaises((ValueError, TypeError, AttributeError)):
            parent_node.to_html()

    def test_parent_node_empty_children(self):
        """ParentNode should handle empty children list"""
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_parent_node_multiple_children(self):
        """ParentNode should render multiple children correctly"""
        child1 = LeafNode("span", "First")
        child2 = LeafNode("span", "Second")
        child3 = LeafNode("span", "Third")
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>First</span><span>Second</span><span>Third</span></div>"
        )

    def test_parent_node_with_props(self):
        """ParentNode should include props in HTML output"""
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], props={"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>child</span></div>'
        )

    def test_parent_node_nested_parents(self):
        """ParentNode should handle deeply nested parent nodes"""
        leaf = LeafNode("span", "text")
        level3 = ParentNode("div", [leaf])
        level2 = ParentNode("section", [level3])
        level1 = ParentNode("main", [level2])
        self.assertEqual(
            level1.to_html(),
            "<main><section><div><span>text</span></div></section></main>"
        )

    def test_parent_node_mixed_children(self):
        """ParentNode should handle mix of LeafNode and ParentNode children"""
        leaf1 = LeafNode("b", "bold")
        parent_child = ParentNode("span", [LeafNode("i", "italic")])
        leaf2 = LeafNode("u", "underline")
        parent_node = ParentNode("div", [leaf1, parent_child, leaf2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>bold</b><span><i>italic</i></span><u>underline</u></div>"
        )

    def test_parent_node_with_special_characters(self):
        """ParentNode should preserve special characters in child text"""
        child = LeafNode("span", "Hello & <goodbye>")
        parent_node = ParentNode("div", [child])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>Hello & <goodbye></span></div>"
        )

    def test_parent_node_child_with_props(self):
        """ParentNode should render children with their own props"""
        child = LeafNode("span", "text", props={"class": "highlight"})
        parent_node = ParentNode("div", [child], props={"class": "wrapper"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="wrapper"><span class="highlight">text</span></div>'
        )

    def test_parent_node_single_child(self):
        """ParentNode should work with a single child"""
        child = LeafNode("p", "paragraph")
        parent_node = ParentNode("article", [child])
        self.assertEqual(parent_node.to_html(), "<article><p>paragraph</p></article>")

    def test_parent_node_empty_tag(self):
        """ParentNode with empty string tag should be treated as having a tag"""
        # Empty string is falsy but different from None
        child = LeafNode("span", "text")
        parent_node = ParentNode("", [child])
        # Should work but produce unusual HTML with empty tag name
        result = parent_node.to_html()
        self.assertIn("text", result)

    def test_parent_node_repr(self):
        """ParentNode should have proper __repr__"""
        child = LeafNode("span", "child")
        parent_node = ParentNode("div", [child], props={"class": "container"})
        repr_str = repr(parent_node)
        self.assertIn("div", repr_str)
        self.assertIn("span", repr_str)
        self.assertIn("container", repr_str)

    def test_parent_node_deeply_nested_with_props(self):
        """ParentNode with deeply nested structure and props at each level"""
        leaf = LeafNode("strong", "text", props={"class": "bold"})
        level2 = ParentNode("em", [leaf], props={"class": "italic"})
        level1 = ParentNode("div", [level2], props={"class": "wrapper"})
        self.assertEqual(
            level1.to_html(),
            '<div class="wrapper"><em class="italic"><strong class="bold">text</strong></em></div>'
        )

    def test_parent_node_multiple_levels_multiple_children(self):
        """ParentNode with multiple children at multiple nesting levels"""
        leaf1 = LeafNode("b", "bold")
        leaf2 = LeafNode("i", "italic")
        inner_parent = ParentNode("span", [leaf1, leaf2])
        leaf3 = LeafNode("u", "underline")
        outer_parent = ParentNode("p", [inner_parent, leaf3])
        self.assertEqual(
            outer_parent.to_html(),
            "<p><span><b>bold</b><i>italic</i></span><u>underline</u></p>"
        )

    def test_parent_node_with_whitespace_in_values(self):
        """ParentNode should preserve whitespace in child values"""
        child = LeafNode("pre", "  line with spaces  ")
        parent_node = ParentNode("div", [child])
        self.assertEqual(
            parent_node.to_html(),
            "<div><pre>  line with spaces  </pre></div>"
        )

    def test_parent_node_children_with_none_tags(self):
        """ParentNode with children that have None tags (text nodes)"""
        child1 = LeafNode(None, "plain text")
        child2 = LeafNode("span", "tagged text")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent_node.to_html(),
            "<div>plain text<span>tagged text</span></div>"
        )

    def test_parent_node_repr_with_children(self):
        """ParentNode repr should properly represent children"""
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child])
        repr_str = repr(parent)
        # repr should contain the tag
        self.assertIn("div", repr_str)

    def test_parent_node_list_is_not_iterable_error(self):
        """Verify ParentNode properly iterates over children list"""
        # This should work without raising an iteration error
        children = [LeafNode("span", "a"), LeafNode("span", "b")]
        parent = ParentNode("div", children)
        result = parent.to_html()
        self.assertIn("<span>a</span>", result)
        self.assertIn("<span>b</span>", result)

    

if __name__ == "__main__":
    unittest.main()