from typing import List, Tuple
from msp_agent.core.generator import load_workflow_from_json
from msp_agent.core.models import Workflow


def validate_workflow(workflow: Workflow) -> Tuple[bool, List[str]]:
    """
    Валидирует структуру Workflow.

    Args:
        workflow: Экземпляр Pydantic модели Workflow.

    Returns:
        Кортеж (is_valid, errors), где:
        - is_valid: True, если workflow валиден, иначе False.
        - errors: Список строк с описаниями ошибок.
    """
    errors: List[str] = []

    # Проверка наличия узлов
    if not workflow.nodes:
        errors.append("Workflow должен содержать хотя бы один узел.")
        # Если нет узлов, дальнейшая проверка бессмысленна
        return False, errors

    # Проверка каждого узла
    node_ids = set()
    for i, node in enumerate(workflow.nodes):
        # Проверка обязательных полей
        if not node.id:
            errors.append(f"Узел {i} не имеет ID.")
        else:
            if node.id in node_ids:
                errors.append(f"Узел с ID '{node.id}' уже существует.")
            node_ids.add(node.id)

        if not node.name:
            errors.append(f"Узел '{node.id}' не имеет имени.")

        if not node.type:
            errors.append(f"Узел '{node.id}' не имеет типа.")

        # Проверка параметров (в данном случае просто проверим, что это словарь)
        if not isinstance(node.parameters.parameters, dict):
            errors.append(f"Параметры узла '{node.id}' должны быть словарем.")

        # Проверка позиции (если задана)
        if node.position is not None:
            if not isinstance(node.position, list) or len(node.position) != 2:
                errors.append(f"Позиция узла '{node.id}' должна быть списком из двух чисел.")
            else:
                if not all(isinstance(coord, int) for coord in node.position):
                    errors.append(f"Координаты позиции узла '{node.id}' должны быть целыми числами.")

    # Проверка соединений
    for i, connection in enumerate(workflow.connections):
        if connection.sourceNodeId not in node_ids:
            errors.append(f"Соединение {i}: sourceNodeId '{connection.sourceNodeId}' не существует.")

        if connection.targetNodeId not in node_ids:
            errors.append(f"Соединение {i}: targetNodeId '{connection.targetNodeId}' не существует.")

        if not isinstance(connection.sourceOutputIndex, int) or connection.sourceOutputIndex < 0:
            errors.append(f"Соединение {i}: sourceOutputIndex должен быть неотрицательным целым числом.")

        if not isinstance(connection.targetOutputIndex, int) or connection.targetOutputIndex < 0:
            errors.append(f"Соединение {i}: targetOutputIndex должен быть неотрицательным целым числом.")

    # Если список ошибок пуст, workflow валиден
    is_valid = len(errors) == 0
    return is_valid, errors