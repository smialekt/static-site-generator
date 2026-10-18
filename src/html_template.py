from typing import Literal, TypedDict, Unpack
from pathlib import Path
import re


TEMPLATE_ELEMENT = Literal["Title", "Content"]


class AllowedKwargs(TypedDict, total=False):
    Title: str
    Content: str


def inject_html_template(template: str, basepath: str | Path, **kwargs: Unpack[AllowedKwargs]) -> str:
    new_template = re.sub(
        r"\{\{\s*(\w+)\s*\}\}",
        lambda m: str(kwargs.get(m.group(1), m.group(0))),
        template,
        flags=re.IGNORECASE
    )
    new_template = new_template.replace(
        'href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    return new_template
