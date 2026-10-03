from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            result.append(node)

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        splitted = node.text.split(delimiter)
        if len(splitted) % 2 == 0:
            raise ValueError("No closing delimiter found. Syntax error")
        if len(splitted) % 2 == 0:
            result.append(node)

        for idx, text_part in enumerate(splitted):
            if text_part:
                type = TextType.TEXT if idx % 2 == 0 else text_type
                result.append(TextNode(text_part, type))

    return result


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
