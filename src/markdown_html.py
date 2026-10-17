from htmlnode import HtmlNode, ParentNode, LeafNode
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
import re


def markdown_to_html_node(md: str) -> HtmlNode:
    blocks = markdown_to_blocks(md)
    content = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.CODE:
                content.append(parse_code(block))
            case BlockType.HEADING:
                content.append(parse_heading(block))
            case BlockType.QUOTE:
                content.append(parse_quote(block))
            case BlockType.UNORDERED_LIST:
                content.append(parse_unordered_list(block))
            case BlockType.ORDERED_LIST:
                content.append(parse_ordered_list(block))
            case BlockType.PARAGRAPH:
                content.append(parse_paragraph(block))

    main_node = ParentNode('div', content)
    return main_node


def parse_paragraph(block_text: str) -> HtmlNode:
    processed_text = " ".join([line.strip()
                              for line in block_text.split('\n')])
    return ParentNode('p', text_to_children(processed_text))


def parse_heading(block_text: str) -> HtmlNode:
    heading_parts = re.findall(r"^(#{1,6})\s+(.+)$", block_text)
    if not heading_parts and len(heading_parts[0]) != 2:
        raise ValueError("Provided text is not proper markdown heading")

    level = block_text.count("#")
    node = ParentNode(
        f"h{level}",
        text_to_children(heading_parts[0][1]),
    )
    return node


def parse_quote(block_text: str) -> HtmlNode:
    children = []
    for line in block_text.split('\n'):
        _, quote_text = line.split(">")
        children.extend(text_to_children(quote_text.strip()))

    node = ParentNode(
        "blockquote",
        children
    )
    return node


def parse_code(block_text: str) -> HtmlNode:
    lines = block_text.split('\n')
    children = []
    _ = lines[1:-1]
    for line in lines[1:-1]:
        text_node = TextNode(line + '\n', TextType.TEXT)
        children.append(text_node_to_html_node(text_node))

    code_node = ParentNode('code', children)
    pre_node = ParentNode('pre', [code_node])
    return pre_node


def parse_unordered_list(block_text: str) -> HtmlNode:
    list_children = []
    for line in block_text.split("\n"):
        _, inner_text = line.split(' ', 1)
        children = text_to_children(inner_text)
        list_children.append(ParentNode(
            'li',
            children,
        ))

    return ParentNode('ul', list_children)


def parse_ordered_list(block_text: str) -> HtmlNode:
    list_children = []
    for line in block_text.split("\n"):
        _, inner_text = line.split(' ', 1)
        children = text_to_children(inner_text)
        list_children.append(ParentNode(
            'li',
            children,
        ))

    return ParentNode('ol', list_children)


def text_to_children(text: str):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]
