Создать CLI-приложение на Typer с модульной архитектурой и базовой поддержкой команд parse, generate, validate. Дополнительно — настроить GitHub Actions для автоматического запуска линтеров и тестов при пуше.

📂 Структура проекта
Код


Копировать
msp-cli/
│
├── cli/
│   ├── __init__.py
│   ├── main.py
│   └── commands/
│       ├── __init__.py
│       ├── parse.py
│       ├── generate.py
│       └── validate.py
│
├── msp_agent/
│   ├── __init__.py
│   ├── core/
│   │   └── __init__.py
│   ├── api/
│   │   └── __init__.py
│   └── templates/
│       └── example.j2
│
├── tests/
│   └── test_cli.py
│
├── configs/
│   └── config.example.yaml
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── pyproject.toml
├── README.md
└── .gitignore
⚙️ Основные файлы
cli/main.py
Python


Копировать
import typer
from cli.commands import parse, generate, validate

app = typer.Typer(help="MSP CLI для управления workflow в N8N")

app.add_typer(parse.app, name="parse")
app.add_typer(generate.app, name="generate")
app.add_typer(validate.app, name="validate")

if __name__ == "__main__":
    app()
cli/commands/parse.py
Python


Копировать
import typer

app = typer.Typer()

@app.command()
def run(input: str = typer.Argument(..., help="Текстовое описание процесса")):
    """
    Парсинг текстового описания в JSON/YAML (заглушка).
    """
    typer.echo(f"Парсим описание: {input}")
cli/commands/generate.py
Python


Копировать
import typer

app = typer.Typer()

@app.command()
def run(file: str = typer.Argument(..., help="JSON файл workflow")):
    """
    Генерация workflow на основе JSON (заглушка).
    """
    typer.echo(f"Генерация workflow из {file}")
cli/commands/validate.py
Python


Копировать
import typer

app = typer.Typer()

@app.command()
def run(file: str = typer.Argument(..., help="JSON файл workflow")):
    """
    Валидация workflow (заглушка).
    """
    typer.echo(f"Валидация {file}")
pyproject.toml
Toml


Копировать
[tool.poetry]
name = "msp-cli"
version = "0.1.0"
description = "MSP CLI для управления N8N workflow"
authors = ["Ваше Имя <email@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.10"
typer = "^0.12"
pydantic = "^2.0"
httpx = "^0.27"
jinja2 = "^3.1"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
black = "^24.0"
ruff = "^0.3"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
README.md
Markdown


Копировать
# MSP CLI

CLI-инструмент для работы с workflow в N8N.

## Установка
```bash
poetry install
```

## Запуск
```bash
poetry run python cli/main.py --help
```

## Примеры
```bash
poetry run python cli/main.py parse "Отправить письмо после получения формы"
poetry run python cli/main.py generate workflow.json
poetry run python cli/main.py validate workflow.json
```
tests/test_cli.py
Python


Копировать
from typer.testing import CliRunner
from cli.main import app

runner = CliRunner()

def test_parse_command():
    result = runner.invoke(app, ["parse", "run", "тест"])
    assert result.exit_code == 0
    assert "Парсим описание" in result.stdout
configs/config.example.yaml
Yaml


Копировать
n8n:
  url: "http://localhost:5678"
  api_key: "your_api_key_here"
.gitignore
Код


Копировать
__pycache__/
*.pyc
.env
.msp/
🚀 CI: GitHub Actions
.github/workflows/ci.yml
Yaml


Копировать
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - name: Install Poetry
        run: pip install poetry
      - name: Install dependencies
        run: poetry install
      - name: Run linters
        run: poetry run ruff check .
      - name: Run tests
        run: poetry run pytest
✅ После копирования:

Bash


Копировать
cd msp-cli
poetry install
poetry run python cli/main.py --help
Команды parse, generate, validate уже работают как заглушки. CI автоматически запускает линтер и тесты при каждом пуше в main.
