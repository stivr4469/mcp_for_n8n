from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class NodeParameter(BaseModel):
    """Параметры для узла workflow."""
    # Например, для HTTP Request это могут быть method, url, headers, body
    # Для Email - to, subject, text
    # Пока делаем максимально гибкую структуру
    parameters: Dict[str, Any] = {}


class WorkflowNode(BaseModel):
    """Описание одного узла в workflow."""
    id: str  # Уникальный идентификатор узла
    name: str  # Имя узла (например, "HTTP Request", "Send Email")
    type: str  # Тип узла (соответствует типу в N8N)
    parameters: NodeParameter  # Параметры узла
    # Позиция на canvas (необязательно для MVP)
    position: Optional[List[int]] = None


class WorkflowConnection(BaseModel):
    """Описание соединения между узлами."""
    sourceNodeId: str
    sourceOutputIndex: int  # Индекс выхода узла-источника (обычно 0 для основного выхода)
    targetNodeId: str
    targetOutputIndex: int  # Индекс входа узла-приемника (обычно 0 для основного входа)


class Workflow(BaseModel):
    """Полное описание workflow."""
    name: str  # Название workflow
    nodes: List[WorkflowNode]  # Список узлов
    connections: List[WorkflowConnection]  # Список соединений между узлами
    # Другие метаданные workflow (необязательно для MVP)
    settings: Optional[Dict[str, Any]] = None