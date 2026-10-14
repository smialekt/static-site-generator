
import unittest

from markdown_html import markdown_to_html_node, parse_code, parse_heading, parse_ordered_list, parse_paragraph, parse_quote, parse_unordered_list
from htmlnode import ParentNode, LeafNode


class TestMarkdownHtml(unittest.TestCase):
    def test_parse_heading(self):
        md = "### Test heading **bold** and _inline_"
        node = parse_heading(md)
        expected = ParentNode(
            "h3",
            [
                LeafNode(None, "Test heading ", {}),
                LeafNode("b", "bold", {}),
                LeafNode(None, " and ", {}),
                LeafNode("i", "inline", {})
            ]
        )
        self.assertEqual(node, expected)

    def test_parse_quote(self):
        md = "> Test _inline_\n>**bold** and a [link](url)"
        node = parse_quote(md)
        expected = ParentNode(
            "blockquote",
            [
                LeafNode(None, "Test ", {}),
                LeafNode("i", "inline", {}),
                LeafNode("b", "bold", {}),
                LeafNode(None, " and a ", {}),
                LeafNode("a", "link", {'href': 'url'})
            ]
        )
        self.assertEqual(node, expected)

    def test_parse_unordered_list(self):
        md = "- test **bold**\n- another `code text`"
        node = parse_unordered_list(md)
        expected = ParentNode(
            "ul",
            [
                ParentNode('li', [
                    LeafNode(None, "test ", {}),
                    LeafNode("b", "bold", {})
                ]),
                ParentNode('li', [
                    LeafNode(None, "another ", {}),
                    LeafNode("code", "code text", {})
                ]),
            ]
        )
        self.assertEqual(node, expected)

    def test_parse_ordered_list(self):
        md = "1. test **bold**\n2. another `code text`"
        node = parse_ordered_list(md)
        expected = ParentNode(
            "ol",
            [
                ParentNode('li', [
                    LeafNode(None, "test ", {}),
                    LeafNode("b", "bold", {})
                ]),
                ParentNode('li', [
                    LeafNode(None, "another ", {}),
                    LeafNode("code", "code text", {})
                ]),
            ]
        )
        self.assertEqual(node, expected)

    def test_parse_code(self):
        md = "```js\ncode block test\n**this should be normal** _this to_\n```"
        node = parse_code(md)
        expected = ParentNode(
            "pre",
            [
                ParentNode('code', [
                    LeafNode(None, "code block test\n", {}),
                    LeafNode(None, "**this should be normal** _this to_\n", {})
                ]),
            ]
        )
        self.assertEqual(node, expected)

    def test_parse_paragraph(self):
        md = "Test paragraph **bolded text** `code text` lol"
        node = parse_paragraph(md)
        expected = ParentNode(
            "p",
            [
                LeafNode(None, "Test paragraph ", {}),
                LeafNode('b', "bolded text", {}),
                LeafNode(None, " ", {}),
                LeafNode('code', "code text", {}),
                LeafNode(None, " lol", {}),
            ]
        )
        self.assertEqual(node, expected)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(
            html,
            expected_html,
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        self.assertEqual(
            html,
            expected_html,
        )

    def test_quote(self):
        md = "> This is a **quote**\n> with multiple lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><blockquote>This is a <b>quote</b>with multiple lines</blockquote></div>"
        self.assertEqual(html, expected_html)

    def test_unordered_list_to_html(self):
        md = "- Item 1 with **bold**\n- Item 2 with _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><ul><li>Item 1 with <b>bold</b></li><li>Item 2 with <i>italic</i></li></ul></div>"
        self.assertEqual(html, expected_html)

    def test_ordered_list_to_html(self):
        md = "1. First item with **bold**\n2. Second item with `code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><ol><li>First item with <b>bold</b></li><li>Second item with <code>code</code></li></ol></div>"
        self.assertEqual(html, expected_html)

