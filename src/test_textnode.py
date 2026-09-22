import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a second text node",
                         TextType.ITALIC, 'www.wikipedia.org')
        self.assertNotEqual(node, node2)

    def test_not_eq_different_obj(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, [])

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(
            "TextNode('This is a text node', bold, '')", node.__repr__())

    def test_repr_with_url(self):
        node = TextNode("This is a text node", TextType.CODE, 'test url')
        self.assertEqual(
            "TextNode('This is a text node', code, 'test url')", node.__repr__())


if __name__ == "__main__":
    unittest.main()
