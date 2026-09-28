import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_raises_syntax_error(self):
        old_nodes = [
            TextNode('Text `code invalid', TextType.TEXT)
        ]
        with self.assertRaises(ValueError, msg='No closing delimiter found. Syntax error'):
            split_nodes_delimiter(old_nodes, '`', TextType.CODE)

    def test_split_nodes_code(self):
        old_nodes = [
            TextNode('Text `code` valid', TextType.TEXT)
        ]
        expected = [
            TextNode('Text ', TextType.TEXT),
            TextNode('code', TextType.CODE),
            TextNode(' valid', TextType.TEXT)
        ]
        self.assertEqual(
            expected,
            split_nodes_delimiter(old_nodes, '`', TextType.CODE)
        )

    def test_split_nodes_bold(self):
        old_nodes = [
            TextNode('Text **bold** valid **another**', TextType.TEXT)
        ]
        expected = [
            TextNode('Text ', TextType.TEXT),
            TextNode('bold', TextType.BOLD),
            TextNode(' valid ', TextType.TEXT),
            TextNode('another', TextType.BOLD),
        ]
        self.assertEqual(
            expected,
            split_nodes_delimiter(old_nodes, '**', TextType.BOLD)
        )

    def text_only_italic(self):
        old_nodes = [
            TextNode('_italic_', TextType.TEXT)
        ]
        expected = [
            TextNode('italic', TextType.ITALIC),
        ]
        self.assertEqual(
            expected,
            split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        )
