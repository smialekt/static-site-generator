from enum import Enum

import re


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    return [s for block in blocks if (s := block.strip())]


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if len(lines) == 1 and re.match(r"^(#{1,6})\s+(.+)$", lines[0]):
        return BlockType.HEADING
    if is_unordered_list(lines):
        return BlockType.UNORDERED_LIST
    if is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    if is_quote(lines):
        return BlockType.QUOTE
    if is_code_block(lines):
        return BlockType.CODE

    return BlockType.PARAGRAPH


def is_code_block(lines: list[str]) -> bool:
    if len(lines) < 3 or len(lines) % 2 != 1:
        return False

    if not lines[0].startswith("```") and not lines[-1].startswith("```"):
        return False

    return True


def is_unordered_list(lines: list[str]) -> bool:
    for line in lines:
        if not line.startswith("- "):
            return False

    return True


def is_ordered_list(lines: list[str]) -> bool:
    for (idx, line) in enumerate(lines, 1):
        if not line.startswith(f"{idx}. "):
            return False

    return True


def is_quote(lines: list[str]) -> bool:
    for line in lines:
        if not line.startswith(">"):
            return False

    return True
