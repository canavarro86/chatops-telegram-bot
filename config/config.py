# config/config.py

import os
import yaml
from types import SimpleNamespace

CONFIG_PATH = os.getenv("CONFIG_PATH", "config/config.yaml")

def load_config(path: str = CONFIG_PATH) -> SimpleNamespace:
    """
    Загружает YAML-конфиг и возвращает объект с атрибутами.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    # Преобразуем dict в Namespace для удобства dot-notation
    return SimpleNamespace(**data)

# Загружаем конфиг сразу при импорте
SETTINGS = load_config()
