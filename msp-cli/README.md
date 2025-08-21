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

## Конфигурация

Создайте файл `configs/config.yaml`, скопировав `configs/config.example.yaml` и заполнив его вашими данными:
- `n8n.url`: URL вашего сервера N8N (например, `http://localhost:5678`).
- `n8n.api_key`: Ваш API ключ N8N.

API ключ также можно задать через переменную окружения `MSP_N8N_API_KEY`.

## Примеры
```bash
# 1. Парсинг текстового описания в промежуточный JSON
poetry run python cli/main.py parse "Отправить письмо после получения формы" --output my_workflow.json

# 2. Генерация N8N-совместимого JSON из промежуточного файла
poetry run python cli/main.py generate my_workflow.json --output n8n_workflow.json

# 3. Валидация промежуточного JSON файла
poetry run python cli/main.py validate my_workflow.json

# 4. Деплой сгенерированного N8N workflow в N8N
poetry run python cli/main.py deploy n8n_workflow.json

# 4.1. Деплой с указанием имени workflow в N8N
poetry run python cli/main.py deploy n8n_workflow.json --name "Мой новый workflow"
```