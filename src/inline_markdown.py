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


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        text_to_track = node.text
        links = extract_markdown_links(text_to_track)
        if len(links) < 1:
            result.append(node)
            continue

        for (link_text, link_url) in links:
            (new_nodes, new_text_to_track) = _split_nodes_helper(
                link_text,
                link_url,
                f"[{link_text}]({link_url})",
                TextType.LINK,
                text_to_track
            )
            text_to_track = new_text_to_track
            result.extend(new_nodes)

    return result


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        text_to_track = node.text
        images = extract_markdown_images(text_to_track)
        if len(images) < 1:
            result.append(node)
            continue

        for (image_text, image_url) in images:
            (new_nodes, new_text_to_track) = _split_nodes_helper(
                image_text,
                image_url,
                f"![{image_text}]({image_url})",
                TextType.IMAGE,
                text_to_track
            )
            text_to_track = new_text_to_track
            result.extend(new_nodes)

    return result


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def _split_nodes_helper(text: str, url: str, delimiter: str, type: TextType, text_to_track: str) -> tuple[list[TextNode], str]:
    results = []
    inner_text_to_track = text_to_track
    parts = text_to_track.split(delimiter, 1)
    if len(parts) == 0:
        return (results, inner_text_to_track)

    if parts[0]:
        results.append(TextNode(parts[0], TextType.TEXT))

    if len(parts) == 2:
        results.append(TextNode(text, type, url))
        inner_text_to_track = parts[1]

    return (results, inner_text_to_track)
