import unittest
from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_empty_tag_raises_exception(self):
        child_node = LeafNode("span", "Child")
        parent_node = ParentNode("", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_emtpy_children_raises_exception(self):
        parent_node = ParentNode("", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()
