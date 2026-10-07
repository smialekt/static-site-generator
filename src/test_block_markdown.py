import unittest

from block_markdown import block_to_block_type, markdown_to_blocks, BlockType


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [],)

    def test_block_to_block_type(self):
        blocks = [
            "This is paragraph",
            "- This is a list\n- with items",
            "1. This is a\n2. Ordered list\n3. Of items",
            "```tcl\nThis is a code block\n```",
            "> this is quote",
            ">this is also a quote\n> but different",
            "# Heading 1",
            "#### also a heading",
            "3. not a list\n4. lol",
            "1.also not a list\n2. ???",
            "-not a list\n- either",
            "######NOT A HEADING??"
        ]
        result = [block_to_block_type(block) for block in blocks]
        print(result)
        print(len(result))
        self.assertEqual(
            result,
            [
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.CODE,
                BlockType.QUOTE,
                BlockType.QUOTE,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ]
        )
