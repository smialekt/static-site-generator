class HtmlNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HtmlNode] | None = None,
        props: dict[str, str] | None = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return "".join(f' {key}="{val}"' for key, val in self.props.items())

    def __repr__(self) -> str:
        return (
            f"HtmlNode(tag={self.tag!r}, value={self.value!r}, "
            f"children={self.children!r}, props={self.props!r})"
        )


class LeafNode(HtmlNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("LeafNode has to have value")
        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return (
            f"HtmlNode(tag={self.tag!r}, value={self.value!r}, "
            f"props={self.props!r})"
        )


class ParentNode(HtmlNode):
    def __init__(
        self,
        tag: str,
        children: list[HtmlNode],
        props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError('ParentNode has to have tag')
        if not self.children:
            raise ValueError('ParentNode has to have children')

        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
