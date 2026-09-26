import unittest
from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_to_html_not_implemented(self):
        node = HtmlNode("p", "Test", None, None)
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_none_props_to_html(self):
        node = HtmlNode("p", "Test", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_empty_props_to_html(self):
        node = HtmlNode("p", "Test", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html(self):
        node = HtmlNode("p", "Test", None, {
            "href": "www.onet.pl",
            "style": "color: black; position: top"
        })
        self.assertEqual(
            node.props_to_html(),
            ' href="www.onet.pl" style="color: black; position: top"'
        )

    def test_repr(self):
        node = HtmlNode(
            "p",
            "Test",
            [HtmlNode("a", "Test value", None, {})],
            {
                "href": "www.onet.pl",
                "style": "color: black; position: top"
            }
        )

        expected = (
            "HtmlNode(tag='p', value='Test', "
            "children=[HtmlNode(tag='a', value='Test value', children=None, props={})], "
            "props={'href': 'www.onet.pl', 'style': 'color: black; position: top'})"
        )
        self.assertEqual(repr(node), expected)


if __name__ == "__main__":
    unittest.main()
