import typer
import json
from pathlib import Path
from msp_agent.core.generator import load_workflow_from_json, generate_n8n_workflow
from msp_agent.core.config import load_config

app = typer.Typer()


@app.command()
def run(
    file: str = typer.Argument(..., help="JSON файл workflow (созданный командой parse)"),
    output: str = typer.Option("n8n_workflow.json", help="Имя выходного JSON файла для N8N")
):
    """
    Генерация workflow на основе JSON.
    """
    typer.echo(f"Генерация workflow из {file}")

    # Загружаем конфигурацию
    config = load_config()
    typer.echo(f"Используемый URL N8N: {config.n8n.url}")
    # В дальнейшем здесь можно будет использовать config.n8n.api_key для аутентификации

    # Путь к файлу и шаблонам
    input_path = Path(file)
    templates_path = Path(__file__).parent.parent.parent / "msp_agent" / "templates"
    output_path = Path(output)

    # Загружаем workflow из JSON
    workflow = load_workflow_from_json(input_path)

    # Генерируем N8N workflow
    n8n_workflow = generate_n8n_workflow(workflow, templates_path)

    # Сохраняем в файл
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(n8n_workflow, f, ensure_ascii=False, indent=2)

    typer.echo(f"N8N workflow сохранен в {output_path.absolute()}")