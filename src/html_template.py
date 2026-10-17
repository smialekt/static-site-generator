from typing import Literal, TypedDict, Unpack
import re


TEMPLATE_ELEMENT = Literal["Title", "Content"]


class AllowedKwargs(TypedDict, total=False):
    Title: str
    Content: str


def inject_html_template(template: str, **kwargs: Unpack[AllowedKwargs]) -> str:
    return re.sub(
        r"\{\{\s*(\w+)\s*\}\}",
        lambda m: str(kwargs.get(m.group(1), m.group(0))),
        template,
        flags=re.IGNORECASE
    )
