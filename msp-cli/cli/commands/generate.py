import typer

app = typer.Typer()

@app.command()
def run(file: str = typer.Argument(..., help="JSON файл workflow")):
    """
    Генерация workflow на основе JSON (заглушка).
    """
    typer.echo(f"Генерация workflow из {file}")