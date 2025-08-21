import os
from pathlib import Path
from typing import Optional
import yaml
from pydantic import BaseModel, Field


class N8nConfig(BaseModel):
    """Конфигурация для N8N."""
    url: str = Field(default="http://localhost:5678", description="URL сервера N8N")
    api_key: Optional[str] = Field(default=None, description="API ключ для N8N")


class Config(BaseModel):
    """Основная конфигурация приложения."""
    n8n: N8nConfig = Field(default_factory=N8nConfig)


def load_config(config_path: Path = Path("configs/config.yaml")) -> Config:
    """
    Загружает конфигурацию из YAML файла.

    Args:
        config_path: Путь к файлу конфигурации.

    Returns:
        Объект Config.
    """
    config_data = {}
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f) or {}

    # Переопределение значений из переменных окружения
    # Например, MSP_N8N_URL и MSP_N8N_API_KEY
    env_n8n_url = os.getenv("MSP_N8N_URL")
    if env_n8n_url:
        config_data.setdefault("n8n", {})["url"] = env_n8n_url

    env_n8n_api_key = os.getenv("MSP_N8N_API_KEY")
    if env_n8n_api_key:
        config_data.setdefault("n8n", {})["api_key"] = env_n8n_api_key

    # Создание объекта Config с дефолтными значениями и переопределением из файла/окружения
    return Config(**config_data)