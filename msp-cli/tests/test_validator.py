import pytest
from msp_agent.core.validator import validate_workflow
from msp_agent.core.models import Workflow, WorkflowNode, WorkflowConnection, NodeParameter


def test_validate_workflow_valid():
    """Тест для валидного workflow."""
    workflow = Workflow(
        name="Валидный workflow",
        nodes=[
            WorkflowNode(
                id="1",
                name="Httprequest",
                type="n8n-nodes-base.httpRequest",
                parameters=NodeParameter(parameters={"description": "Тест"})
            )
        ],
        connections=[]
    )

    is_valid, errors = validate_workflow(workflow)

    assert is_valid is True
    assert len(errors) == 0


def test_validate_workflow_no_nodes():
    """Тест для workflow без узлов."""
    workflow = Workflow(
        name="Workflow без узлов",
        nodes=[],
        connections=[]
    )

    is_valid, errors = validate_workflow(workflow)

    assert is_valid is False
    assert "должен содержать хотя бы один узел" in errors[0]


def test_validate_workflow_node_missing_id():
    """Тест для workflow с узлом без ID."""
    workflow = Workflow(
        name="Workflow с узлом без ID",
        nodes=[
            WorkflowNode(
                id="",
                name="Httprequest",
                type="n8n-nodes-base.httpRequest",
                parameters=NodeParameter(parameters={"description": "Тест"})
            )
        ],
        connections=[]
    )

    is_valid, errors = validate_workflow(workflow)

    assert is_valid is False
    assert "не имеет ID" in errors[0]


def test_validate_workflow_node_duplicate_id():
    """Тест для workflow с дублирующимися ID узлов."""
    workflow = Workflow(
        name="Workflow с дублирующимися ID",
        nodes=[
            WorkflowNode(
                id="1",
                name="Httprequest1",
                type="n8n-nodes-base.httpRequest",
                parameters=NodeParameter(parameters={"description": "Тест1"})
            ),
            WorkflowNode(
                id="1", # Дубликат
                name="Httprequest2",
                type="n8n-nodes-base.httpRequest",
                parameters=NodeParameter(parameters={"description": "Тест2"})
            )
        ],
        connections=[]
    )

    is_valid, errors = validate_workflow(workflow)

    assert is_valid is False
    assert "уже существует" in errors[0]


def test_validate_workflow_connection_invalid_node_id():
    """Тест для workflow с невалидным ID узла в соединении."""
    workflow = Workflow(
        name="Workflow с невалидным соединением",
        nodes=[
            WorkflowNode(
                id="1",
                name="Httprequest",
                type="n8n-nodes-base.httpRequest",
                parameters=NodeParameter(parameters={"description": "Тест"})
            )
        ],
        connections=[
            WorkflowConnection(
                sourceNodeId="1",
                sourceOutputIndex=0,
                targetNodeId="2", # Несуществующий ID
                targetOutputIndex=0
            )
        ]
    )

    is_valid, errors = validate_workflow(workflow)

    assert is_valid is False
    assert "не существует" in errors[0]