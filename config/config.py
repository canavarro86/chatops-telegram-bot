# config/config.py

import os
import yaml
from types import SimpleNamespace

# Пути, по которым ищем файл конфигурации:
# 1) переменная окружения CONFIG_PATH, если задана
# 2) файл config/config.yml
# 3) файл config/config.yaml
DEFAULT_PATHS = [
    os.getenv("CONFIG_PATH"),
    "config/config.yml",
    "config/config.yaml",
]


def load_config() -> SimpleNamespace:
    """
    Загружает конфигурацию из первого найденного файла YAML.

    :return: объект SimpleNamespace с атрибутами из YAML
    :raises FileNotFoundError: если ни один из файлов не найден
    """
    # Ищем первый существующий путь из списка DEFAULT_PATHS
    path = next((p for p in DEFAULT_PATHS if p and os.path.exists(p)), None)
    if path is None:
        raise FileNotFoundError(f"Config file not found. Searched: {DEFAULT_PATHS}")

    # Открываем файл в кодировке UTF-8 и читаем через safe_load
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Преобразуем словарь в объект с атрибутами
    return SimpleNamespace(**data)


# Глобальная переменная SETTINGS: хранит весь конфиг в виде атрибутов
SETTINGS = load_config()
