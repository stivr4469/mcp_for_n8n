import pytest
from msp_agent.core.parser import _identify_node_type, parse_text_to_workflow


def test_identify_node_type_http():
    """Тест для определения типа HTTP Request."""
    assert _identify_node_type("Получить данные с сайта") == "n8n-nodes-base.httpRequest"
    assert _identify_node_type("Отправить HTTP запрос") == "n8n-nodes-base.httpRequest"
    assert _identify_node_type("Заполнить форму") == "n8n-nodes-base.httpRequest"


def test_identify_node_type_email():
    """Тест для определения типа Email."""
    assert _identify_node_type("Отправить письмо") == "n8n-nodes-base.email"
    assert _identify_node_type("Уведомить пользователя по email") == "n8n-nodes-base.email"
    assert _identify_node_type("Письмо с подтверждением") == "n8n-nodes-base.email"


def test_identify_node_type_function():
    """Тест для определения типа Function."""
    assert _identify_node_type("Выполнить функцию") == "n8n-nodes-base.function"
    assert _identify_node_type("Обработать данные в функции") == "n8n-nodes-base.function"


def test_identify_node_type_unknown():
    """Тест для неизвестного типа."""
    assert _identify_node_type("Сделать что-то необычное") is None
    assert _identify_node_type("") is None


def test_parse_text_to_workflow_single_node():
    """Тест для парсинга текста в workflow с одним узлом."""
    input_text = "Отправить письмо пользователю"
    workflow = parse_text_to_workflow(input_text)

    assert workflow.name == "Отправить письмо"
    assert len(workflow.nodes) == 1
    assert len(workflow.connections) == 0
    node = workflow.nodes[0]
    assert node.id == "1"
    assert node.name == "Email"
    assert node.type == "n8n-nodes-base.email"
    assert node.parameters.parameters["description"] == input_text


def test_parse_text_to_workflow_unknown_action():
    """Тест для парсинга текста с неизвестным действием."""
    input_text = "Сделать что-то необычное"
    workflow = parse_text_to_workflow(input_text)

    assert workflow.name == "Сделать что-то"
    assert len(workflow.nodes) == 1
    node = workflow.nodes[0]
    assert node.name == "UnknownAction"
    assert node.type == "n8n-nodes-base.unknown"
    assert node.parameters.parameters["description"] == input_text