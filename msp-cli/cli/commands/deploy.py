import typer
import json
from pathlib import Path
from msp_agent.core.config import load_config
import httpx
from typing import Optional

app = typer.Typer()


@app.command()
def run(
    file: str = typer.Argument(..., help="JSON файл workflow для деплоя (сгенерированный командой 'generate')"),
    name: Optional[str] = typer.Option(None, help="Название для workflow в N8N (по умолчанию берется из файла)")
):
    """
    Деплой workflow в N8N через API.
    """
    config = load_config()
    if not config.n8n.api_key:
        typer.echo("Ошибка: API ключ N8N не найден в конфигурации или переменных окружения (MSP_N8N_API_KEY).")
        raise typer.Exit(code=1)

    file_path = Path(file)
    if not file_path.exists():
        typer.echo(f"Ошибка: Файл {file_path} не найден.")
        raise typer.Exit(code=1)

    # Загружаем workflow из JSON файла
    # Предполагаем, что это уже сгенерированный N8N JSON
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            n8n_workflow_data = json.load(f)
    except json.JSONDecodeError as e:
        typer.echo(f"Ошибка: Невалидный JSON в файле {file_path}: {e}")
        raise typer.Exit(code=1)

    # Устанавливаем имя, если оно указано
    if name:
        n8n_workflow_data["name"] = name

    # Подготавливаем запрос
    url = f"{config.n8n.url.rstrip('/')}/api/v1/workflows"
    headers = {
        "Authorization": f"Bearer {config.n8n.api_key}",
        "Content-Type": "application/json"
    }

    # Отправляем запрос
    try:
        typer.echo(f"Отправка workflow в {url}...")
        response = httpx.post(url, json=n8n_workflow_data, headers=headers, timeout=30)
        response.raise_for_status()  # Вызовет исключение для 4xx и 5xx статусов
        created_workflow = response.json()
        typer.echo(f"Workflow успешно создан/обновлен. ID: {created_workflow['id']}")
    except httpx.HTTPStatusError as e:
        typer.echo(f"Ошибка HTTP при деплое: {e.response.status_code} - {e.response.text}")
        raise typer.Exit(code=1)
    except httpx.RequestError as e:
        typer.echo(f"Ошибка сети при деплое: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Неожиданная ошибка при деплое: {e}")
        raise typer.Exit(code=1)