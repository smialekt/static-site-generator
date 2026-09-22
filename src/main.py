from textnode import TextNode, TextType


def main():
    text_node = TextNode('test text', TextType.BOLD, 'url')
    print(text_node)


if __name__ == '__main__':
    main()
