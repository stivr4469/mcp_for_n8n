import typer

app = typer.Typer()

@app.command()
def run(file: str = typer.Argument(..., help="JSON файл workflow")):
    """
    Валидация workflow (заглушка).
    """
    typer.echo(f"Валидация {file}")