import typer
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import json
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
import tomli
from pydantic import BaseModel


from er_api_interface import ERApiDirector

app = typer.Typer()
console = Console()

# Load environment variables from .secrets.toml file in the ./models/ directory
with open("./models/.secrets.toml", "rb") as f:
    secrets = tomli.load(f)
    # Get/set the supabase URL and key from the secrets File
    SUPABASE_URL = secrets["supabase"]["url"]
    SUPABASE_KEY = secrets["supabase"]["key"]


@app.command()
def fetch_and_push(
    models: Optional[List[str]] = typer.Option(
        None,
        "--models",
        "-m",
        help="Specific models to fetch and push. If not provided, all models will be processed.",
    ),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file name for the fetched data. If not provided, data won't be saved to a file.",
    ),
    push: bool = typer.Option(
        True,
        "--push/--no-push",
        help="Push data to Supabase after fetching. Default is True.",
    ),
    display: bool = typer.Option(
        False, "--display", "-d", help="Display fetched data summary in the console."
    ),
):
    """
    Fetch data from the ER API and optionally push it to Supabase.
    """
    director = ERApiDirector()

    with Progress() as progress:
        fetch_task = progress.add_task("[cyan]Fetching data...", total=100)

        if models:
            data = director.build_specific(models)
        else:
            data = director.build_all()

        progress.update(fetch_task, completed=100)

    if output:
        for model, items in data.items():
            with open(output, "w") as f:
                json.dump({model: [item.model_dump_json() for item in items]}, f)
        console.print(f"[green]Data saved to {output}[/green]")

    if display:
        display_data(data)

    if push:
        push_to_supabase(data, models)


def display_data(data: dict):
    """
    Display fetched data in a table format.
    """
    table = Table(title="Fetched Data Summary")
    table.add_column("Model", style="cyan")
    table.add_column("Items Count", style="magenta")

    for model, items in data.items():
        table.add_row(model, str(len(items)))

    console.print(table)


def push_to_supabase(data: dict[str, list[BaseModel]], models: Optional[List[str]] = None):
    """
    Push fetched data to Supabase.
    """
    models_to_push = models or list(data.keys())

    # Initialize Supabase client
    supabase: Client = create_client(
        SUPABASE_URL, SUPABASE_KEY, options=ClientOptions(schema="meta")
    )

    with Progress() as progress:
        overall_task = progress.add_task(
            "[cyan]Pushing data to Supabase...", total=len(models_to_push)
        )

        for model in models_to_push:
            if model not in data:
                console.print(
                    f"[yellow]Warning: Model '{model}' not found in the fetched data. Skipping.[/yellow]"
                )
                progress.update(overall_task, advance=1)
                continue

            model_data = data[model]
            table_name = (
                f"er_{model.lower()}"  # Assuming table names follow this convention
            )

            model_task = progress.add_task(
                f"[green]Pushing {model} data...", total=len(model_data)
            )

            for item in model_data:
                try:
                    # Upsert data to Supabase
                    supabase.table(table_name).upsert(item.model_dump()).execute()
                    progress.update(model_task, advance=1)
                except Exception as e:
                    console.print(
                        f"[red]Error pushing item to {table_name}: {str(e)}[/red]"
                    )

            progress.update(overall_task, advance=1)

    console.print("[green]Data push to Supabase completed![/green]")


@app.command()
def list_models():
    """
    List all available models that can be fetched.
    """
    director = ERApiDirector()
    models = list(director.builders.keys())

    table = Table(title="Available Models")
    table.add_column("Model Name", style="cyan")

    for model in models:
        table.add_row(model)

    console.print(table)


if __name__ == "__main__":
    app()
