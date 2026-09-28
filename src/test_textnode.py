import unittest
from textnode import TextNode, TextType, text_node_to_html_node


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
            "TextNode('This is a text node', b, '')", node.__repr__())

    def test_repr_with_url(self):
        node = TextNode("This is a text node", TextType.CODE, 'test url')
        self.assertEqual(
            "TextNode('This is a text node', code, 'test url')", node.__repr__())

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code node")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, 'www.onet.pl')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.props, {
            'href': 'www.onet.pl',
        })
        self.assertEqual(html_node.value, "This is a link node")

    def test_image(self):
        node = TextNode("This is a image node",
                        TextType.IMAGE, '/path/img.jpg')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props, {
            'src': '/path/img.jpg',
            'alt': 'This is a image node'
        })
        self.assertEqual(html_node.value, "")


if __name__ == "__main__":
    unittest.main()
