import json
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader
from msp_agent.core.models import Workflow


def load_workflow_from_json(file_path: Path) -> Workflow:
    """Загружает workflow из JSON файла и парсит его в Pydantic модель."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return Workflow(**data)


def _get_template_name(node_type: str) -> str:
    """Определяет имя шаблона на основе типа узла."""
    # Простое сопоставление типов узлов с именами шаблонов
    type_to_template = {
        "n8n-nodes-base.httpRequest": "http_request.j2",
        "n8n-nodes-base.email": "email.j2",
        # Можно добавить больше сопоставлений
    }
    # Если тип не найден, используем шаблон по умолчанию
    return type_to_template.get(node_type, "unknown.j2")


def generate_n8n_workflow(workflow: Workflow, templates_dir: Path) -> Dict[str, Any]:
    """
    Генерирует полный JSON-файл workflow N8N на основе Pydantic модели.

    Args:
        workflow: Экземпляр Pydantic модели Workflow.
        templates_dir: Путь к директории с Jinja2 шаблонами.

    Returns:
        Словарь, представляющий JSON-файл workflow N8N.
    """
    # Настройка Jinja2
    env = Environment(loader=FileSystemLoader(templates_dir))

    # Генерация JSON для каждого узла
    nodes_data: List[Dict[str, Any]] = []
    for node in workflow.nodes:
        template_name = _get_template_name(node.type)
        template = env.get_template(template_name)
        # Рендерим шаблон с параметрами узла
        node_json_str = template.render(node=node)
        # Парсим обратно в словарь
        node_data = json.loads(node_json_str)
        nodes_data.append(node_data)

    # Формирование полного JSON-файла workflow N8N
    # Это базовая структура, в реальном проекте может быть сложнее
    n8n_workflow = {
        "name": workflow.name,
        "nodes": nodes_data,
        "connections": workflow.connections,
        "active": False, # По умолчанию workflow не активен
        "settings": workflow.settings or {},
        "versionId": "placeholder_version_id" # Заглушка
    }

    return n8n_workflow