import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


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

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK,
                         "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE,
                         "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_with_no_links(self):
        node = TextNode(
            "This is a text with no links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a text with no links", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_with_no_images(self):
        node = TextNode(
            "This is a text with no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a text with no images", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_only(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK,
                         "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_imaeges_only(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image",
                         TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE,
                     "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), nodes)

    def test_text_to_textnodes_normal_string(self):
        text = "String with no md"
        nodes = [
            TextNode("String with no md", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnodes(text), nodes)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = []
        self.assertEqual(text_to_textnodes(text), nodes)

    def test_text_to_textnodes_all_formatted(self):
        text = "**bold**_italic_"
        nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC)
        ]
        self.assertEqual(text_to_textnodes(text), nodes)

    def test_text_to_textnodes_unsupported_delimiter(self):
        text = "'unsupported' hello world"
        nodes = [
            TextNode("'unsupported' hello world", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), nodes)

    def test_text_to_textnodes_syntax_error(self):
        text = "**bold* _italic"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)
