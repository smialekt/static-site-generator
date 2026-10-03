import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = [
            ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
            ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')
        ]
        self.assertEqual(extract_markdown_images(text), matches)

    def test_extract_markdown_images_empty(self):
        text = "There are no images [ ) []"
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = [
            ('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),
            ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')
        ]
        self.assertEqual(extract_markdown_links(text), matches)

    def test_extract_markdown_links_empty(self):
        text = "There are no links [ ) []"
        self.assertEqual(extract_markdown_links(text), [])
