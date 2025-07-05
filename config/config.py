# config/config.py

import os
import yaml
from types import SimpleNamespace

# Попробуем сначала .yml, потом .yaml
DEFAULT_PATHS = [
    os.getenv("CONFIG_PATH"),            # если задано в env
    "config/config.yml",
    "config/config.yaml"
]

def load_config() -> SimpleNamespace:
    path = next((p for p in DEFAULT_PATHS if p and os.path.exists(p)), None)
    if path is None:
        raise FileNotFoundError(f"Config file not found. Searched: {DEFAULT_PATHS}")
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return SimpleNamespace(**data)

SETTINGS = load_config()

