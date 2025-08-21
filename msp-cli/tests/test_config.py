import os
import pytest
from pathlib import Path
from msp_agent.core.config import load_config, Config, N8nConfig


def test_load_config_default():
    """Тест для загрузки конфигурации с дефолтными значениями."""
    # Используем несуществующий путь, чтобы конфигурация бралась из дефолтов
    config = load_config(Path("nonexistent_config.yaml"))

    assert isinstance(config, Config)
    assert isinstance(config.n8n, N8nConfig)
    assert config.n8n.url == "http://localhost:5678"
    assert config.n8n.api_key is None


def test_load_config_from_file(tmp_path):
    """Тест для загрузки конфигурации из файла."""
    config_data = {
        "n8n": {
            "url": "http://test.n8n.local:5678",
            "api_key": "test_api_key"
        }
    }
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, 'w', encoding='utf-8') as f:
        import yaml
        yaml.dump(config_data, f)

    config = load_config(config_file)

    assert config.n8n.url == "http://test.n8n.local:5678"
    assert config.n8n.api_key == "test_api_key"


def test_load_config_override_with_env(monkeypatch, tmp_path):
    """Тест для переопределения конфигурации переменными окружения."""
    # Устанавливаем переменные окружения
    monkeypatch.setenv("MSP_N8N_URL", "http://env.n8n.local:5678")
    monkeypatch.setenv("MSP_N8N_API_KEY", "env_api_key")

    # Создаем файл конфигурации с другими значениями
    config_data = {
        "n8n": {
            "url": "http://file.n8n.local:5678",
            "api_key": "file_api_key"
        }
    }
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, 'w', encoding='utf-8') as f:
        import yaml
        yaml.dump(config_data, f)

    config = load_config(config_file)

    # Переменные окружения должны переопределить значения из файла
    assert config.n8n.url == "http://env.n8n.local:5678"
    assert config.n8n.api_key == "env_api_key"

    # Очищаем переменные окружения
    monkeypatch.delenv("MSP_N8N_URL")
    monkeypatch.delenv("MSP_N8N_API_KEY")


def test_load_config_partial_override_with_env(monkeypatch, tmp_path):
    """Тест для частичного переопределения конфигурации переменными окружения."""
    # Устанавливаем только URL через переменную окружения
    monkeypatch.setenv("MSP_N8N_URL", "http://env.n8n.local:5678")
    # API ключ не устанавливаем

    # Создаем файл конфигурации
    config_data = {
        "n8n": {
            "url": "http://file.n8n.local:5678",
            "api_key": "file_api_key"
        }
    }
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, 'w', encoding='utf-8') as f:
        import yaml
        yaml.dump(config_data, f)

    config = load_config(config_file)

    # URL должен быть из переменной окружения
    assert config.n8n.url == "http://env.n8n.local:5678"
    # API ключ должен быть из файла
    assert config.n8n.api_key == "file_api_key"

    # Очищаем переменную окружения
    monkeypatch.delenv("MSP_N8N_URL")