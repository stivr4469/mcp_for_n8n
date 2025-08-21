import typer

app = typer.Typer()

@app.command()
def run(input: str = typer.Argument(..., help="Текстовое описание процесса")):
    """
    Парсинг текстового описания в JSON/YAML (заглушка).
    """
    typer.echo(f"Парсим описание: {input}")