from textnode import TextNode, TextType

import os
import shutil
from pathlib import Path


def main():
    copy_folder_content("./static", "./public")


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
