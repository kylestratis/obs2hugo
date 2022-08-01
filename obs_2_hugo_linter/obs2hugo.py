import os
import re

import click


def _ingest_file(filename: str) -> str:
    """
    Opens a markdown file and pulls each block into a data structure
    """
    file_str = ""
    if filename[-3:] != ".md":
        raise click.FileError(
            filename, hint=f"File {filename} is not a markdown file, aborting."
        )
    with open(filename) as f:
        file_str = f.read().rstrip()
    return file_str


def _write_file(rendered: str, filename: str = "index_out.md") -> str:
    with open(filename, "w") as f:
        f.write(rendered)


def _condense_code_fences():
    """
    Detect code fences and put into a single string with newlines?
    """
    raise NotImplementedError


def _remove_yaml():
    raise NotImplementedError


def _convert_images(loaded_file: str):
    return re.sub(
        r"!\[{2}(.+\.(?:png|jpg|jpeg|gif|bmp|svg))\]{2}",
        r"{{<img src=\"\1\">}})",
        loaded_file,
        flags=re.I,
    )


def _insert_spacing(loaded_file: str):
    """
    This extremely ugly Regex detects paragraphs while ignoring lists and mostly ignoring codeblocks
    while adding a newline if there is only one. Code block support is...provisional at best.
    """
    return re.sub(
        r"^((?!(-\s)+|((`{3}\w*\n)([\s\S]*?\n)(`{3}))(?!\n{2,})).+$)\n(?!\n+)",
        r"\1\n\n",
        loaded_file,
        flags=re.M,
    )


@click.command()
@click.argument("input_filename", type=click.Path(dir_okay=False), default="index.md")
@click.option(
    "-t",
    "--test",
    is_flag=True,
    show_default=True,
    default=False,
    help="Prints result to screen instead of writing to file",
)
def main(test, input_filename):
    ingested = _ingest_file(input_filename)
    converted_image = _convert_images(ingested)
    spaced = _insert_spacing(converted_image)
    if test:
        print(spaced)
    else:
        _write_file(rendered=spaced)
