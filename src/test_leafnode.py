import unittest
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props_p(self):
        node = LeafNode("p", "Hello, world!", {'href': 'www.onet.pl'})
        self.assertEqual(
            node.to_html(), "<p href=\"www.onet.pl\">Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(
            node.to_html(), "Hello, world!")

    def test_leaf_no_value_value_error(self):
        node = LeafNode("a", None, {'href': 'www.onet.pl'})  # type: ignore
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = LeafNode("p", "Hello, world!", {'href': 'www.onet.pl'})
        expected = (
            "HtmlNode(tag='p', "
            "value='Hello, world!', "
            "props={'href': 'www.onet.pl'})"
        )
        self.assertEqual(repr(node), expected)


if __name__ == '__main__':
    unittest.main()
