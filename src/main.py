import os
import shutil
from pathlib import Path

from block_markdown import extract_title
from html_template import inject_html_template
from markdown_html import markdown_to_html_node


def main():
    copy_folder_content("./static", "./public")
    generate_pages_recursive("./content", "./template.html", "./public")


def generate_pages_recursive(dir_path_content: str | Path, template_path: str | Path, dest_dir_path):

    for item in os.listdir(dir_path_content):
        new_source_path = os.path.join(dir_path_content, item)

        if os.path.isfile(new_source_path):
            item_path = Path(item)
            new_item_name = item_path.with_suffix('.html')

            generate_page(new_source_path, template_path,
                          os.path.join(dest_dir_path, new_item_name))
        else:
            new_destination_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(
                new_source_path, template_path, new_destination_path)


def generate_page(from_path: str | Path, template_path: str | Path, dest_path: str | Path):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as md:
        md_content = md.read()
    with open(template_path, "r") as template:
        template_content = template.read()

    html_node = markdown_to_html_node(md_content)
    generated_html = html_node.to_html()
    page_title = extract_title(md_content)

    Path(dest_path).parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "w") as final:
        final.write(inject_html_template(
            template_content, Title=page_title, Content=generated_html))


def copy_folder_content(src: str | Path, dest: str | Path) -> None:
    if os.path.isfile(src):
        raise ValueError(f"Source path should be a directory:\n{src}")

    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.makedirs(dest, exist_ok=True)

    if not os.path.isdir(dest):
        raise ValueError(f"Provided destination is not a folder:\n{dest}")

    for item in os.listdir(src):
        source_item_path = os.path.join(src, item)
        destination_item_path = os.path.join(dest, item)
        if os.path.isfile(source_item_path):
            shutil.copy(source_item_path, destination_item_path)
        else:
            copy_folder_content(source_item_path, destination_item_path)


if __name__ == '__main__':
    main()
