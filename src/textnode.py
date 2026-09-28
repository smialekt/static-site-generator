from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = None
    BOLD = 'b'
    ITALIC = 'i'
    CODE = 'code'
    LINK = 'a'
    IMAGE = 'img'


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = '') -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False

        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text!r}, {self.text_type.value}, {self.url!r})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    tag = text_node.text_type.value
    params = {}
    inner_text = text_node.text
    match text_node.text_type:
        case TextType.LINK:
            params = {
                'href': text_node.url
            }
        case TextType.IMAGE:
            params = {
                'src': text_node.url,
                'alt': text_node.text
            }
            inner_text = ''
    return LeafNode(tag, inner_text, params)
