import requests
from config.config import SETTINGS


class CIAPI:
    """
    Клиент для взаимодействия с GitHub Actions API:
    - Запуск workflow по ID или имени файла
    - Получение данных о последнем запуске workflow
    """

    def __init__(self):
        """
        Инициализация клиента:
        - base: базовый URL для GitHub Actions данного репозитория
        - headers: заголовки с авторизацией и версией API
        """
        # Формируем базовый URL для всех запросов к Actions API
        self.base = f"https://api.github.com/repos/{SETTINGS.github_repo}/actions"
        # Заголовки для аутентификации и указания версии API
        self.headers = {
            "Authorization": f"token {SETTINGS.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def trigger_build(self, workflow_id: str, ref: str = "main"):
        """
        Запускает указанный workflow.

        :param workflow_id: ID или имя файла workflow
        :param ref: ветка или SHA, на которой нужно запустить workflow (по умолчанию "main")
        :return: словарь с кодом статуса HTTP и идентификатором workflow
        :raises: HTTPError, если запрос завершился неудачно
        """
        url = f"{self.base}/workflows/{workflow_id}/dispatches"
        payload = {"ref": ref}

        # Отправляем POST-запрос для запуска workflow
        resp = requests.post(url, json=payload, headers=self.headers)
        # Генерируем исключение при ошибочном статусе
        resp.raise_for_status()

        return {"status": resp.status_code, "workflow": workflow_id}

    def get_last_run(self, workflow_id: str):
        """
        Получает информацию о последнем запуске указанного workflow.

        :param workflow_id: ID или имя файла workflow
        :return: словарь с данными последнего запуска или None, если запусков нет
        :raises: HTTPError, если запрос завершился неудачно
        """
        # Запрашиваем только один последний запуск
        url = f"{self.base}/workflows/{workflow_id}/runs?per_page=1"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()

        # Извлекаем список запусков и возвращаем первый элемент, если он есть
        runs = resp.json().get("workflow_runs", [])
        return runs[0] if runs else None
