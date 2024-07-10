import typer
from pathlib import Path
from collections import defaultdict

app = typer.Typer()

def process_file(input_file: Path, filter_prefix: str = None):
    categories = defaultdict(list)

    with input_file.open('r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('┃')
            if len(parts) == 2:
                key = parts[0].split('/', 2)
                if len(key) >= 2:
                    category = f"{key[0].lower()}_{key[1].lower()}"
                    if filter_prefix is None or key[0].lower() == filter_prefix.lower():
                        categories[category].append(line.strip())

    output_dir = input_file.parent / "texts"
    output_dir.mkdir(exist_ok=True)

    for category, lines in categories.items():
        output_file = output_dir / f"{category}.txt"
        with output_file.open('w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    return len(categories)

@app.command()
def split_file(
    input_file: Path = typer.Argument(..., help="Input text file to process"),
    filter_prefix: str = typer.Option(None, help="Filter by prefix (e.g., 'Item')")
):
    """
    Split a text file into multiple files based on categories.
    """
    if not input_file.exists():
        typer.echo(f"Error: Input file '{input_file}' does not exist.")
        raise typer.Exit(code=1)

    num_files = process_file(input_file, filter_prefix)
    typer.echo(f"Successfully created {num_files} output files.")

if __name__ == "__main__":
    app()
