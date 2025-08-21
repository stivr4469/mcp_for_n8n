import re
from typing import List, Optional
from msp_agent.core.models import Workflow, WorkflowNode, WorkflowConnection, NodeParameter


def _identify_node_type(text: str) -> Optional[str]:
    """
    Очень простая функция для определения типа узла на основе текста.
    В реальной реализации здесь будет более сложная логика NLP.
    """
    text_lower = text.lower()
    # Проверяем самые специфичные ключевые слова первыми
    if "http" in text_lower:
        # Тип узла для HTTP Request в N8N
        return "n8n-nodes-base.httpRequest"
    elif "email" in text_lower:
        # Тип узла для Email в N8N
        return "n8n-nodes-base.email"
    elif "function" in text_lower:
        # Тип узла для Function в N8N
        return "n8n-nodes-base.function"
    # Затем проверяем кириллические аналоги
    elif "функци" in text_lower:
        return "n8n-nodes-base.function"
    elif "письм" in text_lower:
        return "n8n-nodes-base.email"
    elif "отправ" in text_lower:
        # Это слово может быть неоднозначным, но для простоты отнесем к email
        return "n8n-nodes-base.email"
    elif "запрос" in text_lower or "форм" in text_lower or "данные" in text_lower:
        # Более общие слова
        return "n8n-nodes-base.httpRequest"
    # Можно добавить больше условий для других типов узлов
    return None


def parse_text_to_workflow(input_text: str) -> Workflow:
    """
    Парсит текстовое описание в объект Workflow.

    Args:
        input_text: Текстовое описание процесса.

    Returns:
        Объект Workflow.
    """
    # Определяем имя workflow из текста (пока просто первые 20 символов, но не обрезаем слова)
    if len(input_text) > 20:
        # Найдем последний пробел в пределах 20 символов
        last_space_index = input_text[:20].rfind(' ')
        if last_space_index != -1:
            workflow_name = input_text[:last_space_index]
        else:
            # Если пробела нет, обрежем жестко
            workflow_name = input_text[:20]
    else:
        workflow_name = input_text

    # Определяем тип узла
    node_type = _identify_node_type(input_text)

    nodes: List[WorkflowNode] = []
    connections: List[WorkflowConnection] = []

    if node_type:
        # Создаем один узел на основе определенного типа
        node = WorkflowNode(
            id="1",  # Для MVP просто "1"
            name=node_type.split(".")[-1].capitalize(),  # Имя из типа, например, "HttpRequest"
            type=node_type,
            parameters=NodeParameter(parameters={"description": input_text})  # Пока просто описание
        )
        nodes.append(node)
    else:
        # Если тип не определен, создаем узел-заглушку
        node = WorkflowNode(
            id="1",
            name="UnknownAction",
            type="n8n-nodes-base.unknown",
            parameters=NodeParameter(parameters={"description": input_text})
        )
        nodes.append(node)

    # Создаем объект workflow
    workflow = Workflow(
        name=workflow_name,
        nodes=nodes,
        connections=connections  # Пока нет соединений для одного узла
    )

    return workflow