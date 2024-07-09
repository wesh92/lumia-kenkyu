import json
import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import glob
import os

convert_app = typer.Typer()
console = Console()

def convert_item_data(input_text):
    lines = input_text.strip().split('\n')
    item_dict = {}

    for line in lines:
        key, value = line.split('┃')
        item_id = key.split('/')[-1]
        item_dict[item_id] = value

    return item_dict

def l10n_converter(filenames: list[str], save: bool = True, use_glob: bool = False):
    """
    Convert l10n files to JSON format.

    :param filenames: List of filenames or glob patterns to convert.
    :param save: Save the converted data to a JSON file. Default is True.
    :param use_glob: Use glob matching for filenames. Default is False.

    :return: Dictionary of converted data.

    Example:
        l10n_converter(["items", "locations"])
        l10n_converter(["weapontype_*"], use_glob=True)

    :raises FileNotFoundError: If the file is not found.
    :raises ValueError: If the file is empty.
    :raises TypeError: If the filename is not a string.
    :raises Exception: If the file is not a valid l10n file.
    """

    converted_data = {}

    for pattern in filenames:
        if use_glob:
            matching_files = glob.glob(f"texts/{pattern}.txt")
        else:
            matching_files = [f"texts/{pattern}.txt"]

        for file_path in matching_files:
            filename = os.path.splitext(os.path.basename(file_path))[0]

            with open(file_path, "r") as f:
                lines = f.readlines()

            if not lines:
                raise ValueError(f"{file_path} is empty.")

            try:
                converted_data[filename] = convert_item_data(''.join(lines))
            except Exception as e:
                raise Exception(f"Error converting {file_path}: {e}")

    if save:
        for filename, data in converted_data.items():
            with open(f"jsons/{filename}.json", "w") as f:
                json.dump(data, f, indent=4)

    return converted_data

@convert_app.command()
def convert_l10n(
    filenames: List[str] = typer.Option(
        [],
        "--filenames",
        "-f",
        help="List of filenames or glob patterns to convert.",
    ),
    save: bool = typer.Option(
        True,
        "--save/--no-save",
        help="Save the converted data to a JSON file. Default is True.",
    ),
    use_glob: bool = typer.Option(
        False,
        "--glob/--no-glob",
        help="Use glob matching for filenames. Default is False.",
    ),
):
    """
    Convert l10n files to JSON format.
    """
    try:
        converted_data = l10n_converter(filenames, save, use_glob)
        console.print(f"[green]Data converted successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error converting data: {e}[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    convert_app()
