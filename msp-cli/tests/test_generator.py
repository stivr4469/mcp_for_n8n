import json
import pytest
from pathlib import Path
from msp_agent.core.generator import load_workflow_from_json, generate_n8n_workflow, _get_template_name
from msp_agent.core.models import Workflow, WorkflowNode, NodeParameter


@pytest.fixture
def sample_workflow_data():
    """Фикстура с данными для тестового workflow."""
    return {
        "name": "Тестовый workflow",
        "nodes": [
            {
                "id": "1",
                "name": "Httprequest",
                "type": "n8n-nodes-base.httpRequest",
                "parameters": {"parameters": {"description": "Тест"}},
                "position": [100, 100]
            }
        ],
        "connections": [],
        "settings": {}
    }


@pytest.fixture
def sample_workflow_file(tmp_path, sample_workflow_data):
    """Фикстура, создающая временный файл с тестовыми данными workflow."""
    file_path = tmp_path / "test_workflow.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sample_workflow_data, f)
    return file_path


def test_load_workflow_from_json(sample_workflow_file, sample_workflow_data):
    """Тест для загрузки workflow из JSON файла."""
    workflow = load_workflow_from_json(sample_workflow_file)

    assert isinstance(workflow, Workflow)
    assert workflow.name == sample_workflow_data["name"]
    assert len(workflow.nodes) == 1
    assert workflow.nodes[0].id == sample_workflow_data["nodes"][0]["id"]


def test_get_template_name():
    """Тест для определения имени шаблона."""
    assert _get_template_name("n8n-nodes-base.httpRequest") == "http_request.j2"
    assert _get_template_name("n8n-nodes-base.email") == "email.j2"
    assert _get_template_name("n8n-nodes-base.unknown") == "unknown.j2"
    assert _get_template_name("some.unknown.type") == "unknown.j2"


def test_generate_n8n_workflow(sample_workflow_data, tmp_path):
    """Тест для генерации N8N workflow."""
    workflow = Workflow(**sample_workflow_data)
    templates_dir = Path(__file__).parent.parent / "msp_agent" / "templates"

    n8n_workflow = generate_n8n_workflow(workflow, templates_dir)

    assert isinstance(n8n_workflow, dict)
    assert n8n_workflow["name"] == workflow.name
    assert len(n8n_workflow["nodes"]) == 1
    generated_node = n8n_workflow["nodes"][0]
    assert generated_node["id"] == workflow.nodes[0].id
    assert generated_node["type"] == workflow.nodes[0].type
    # Проверяем, что параметры из исходного workflow присутствуют
    assert "description" in generated_node["parameters"]
    # Проверяем, что стандартные параметры шаблона также присутствуют
    assert "url" in generated_node["parameters"]
    assert "method" in generated_node["parameters"]