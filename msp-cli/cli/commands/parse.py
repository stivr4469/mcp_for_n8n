import typer
import json
from pathlib import Path
from msp_agent.core.parser import parse_text_to_workflow

app = typer.Typer()


@app.command()
def run(
    input: str = typer.Argument(..., help="Текстовое описание процесса"),
    output: str = typer.Option("workflow.json", help="Имя выходного JSON файла")
):
    """
    Парсинг текстового описания в JSON/YAML.
    """
    typer.echo(f"Парсим описание: {input}")

    # Выполняем парсинг
    workflow = parse_text_to_workflow(input)

    # Подготавливаем данные для сохранения (Pydantic модели нужно сериализовать)
    # Для простоты используем model_dump() из Pydantic v2
    workflow_data = workflow.model_dump()

    # Сохраняем в файл
    output_path = Path(output)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(workflow_data, f, ensure_ascii=False, indent=2)

    typer.echo(f"Workflow сохранен в {output_path.absolute()}")