import typer
from pathlib import Path
from msp_agent.core.generator import load_workflow_from_json
from msp_agent.core.validator import validate_workflow

app = typer.Typer()


@app.command()
def run(file: str = typer.Argument(..., help="JSON файл workflow")):
    """
    Валидация workflow.
    """
    typer.echo(f"Валидация {file}")

    # Путь к файлу
    file_path = Path(file)

    # Загружаем workflow из JSON
    workflow = load_workflow_from_json(file_path)

    # Выполняем валидацию
    is_valid, errors = validate_workflow(workflow)

    if is_valid:
        typer.echo("Workflow валиден.")
    else:
        typer.echo("Workflow НЕ валиден. Ошибки:")
        for error in errors:
            typer.echo(f" - {error}")
        # Завершаем с ненулевым кодом, чтобы indicated failure в скриптах
        raise typer.Exit(code=1)