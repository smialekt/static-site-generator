from functools import partial

from textnode import TextNode, TextType
from htmlnode import HtmlNode
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        splitted = node.text.split(delimiter)
        if len(splitted) % 2 == 0:
            raise ValueError("No closing delimiter found. Syntax error")

        for idx, text_part in enumerate(splitted):
            if text_part:
                type = TextType.TEXT if idx % 2 == 0 else text_type
                result.append(TextNode(text_part, type))

    return result


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def text_to_textnodes(text: str) -> list[TextNode]:
    pipeline = [
        split_nodes_image,
        split_nodes_link,
        partial(split_nodes_delimiter, delimiter="**",
                text_type=TextType.BOLD),
        partial(split_nodes_delimiter, delimiter="_",
                text_type=TextType.ITALIC),
        partial(split_nodes_delimiter, delimiter="`", text_type=TextType.CODE),
    ]
    result = [TextNode(text, TextType.TEXT)]

    for fn in pipeline:
        result = fn(result)

    return result


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    return [s for block in blocks if (s := block.strip())]
