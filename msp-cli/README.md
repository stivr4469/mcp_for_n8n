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