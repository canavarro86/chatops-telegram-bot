# bot/services/github_api.py

import requests
from config.config import SETTINGS


class GitHubAPI:
    """
    Клиент для работы с GitHub Issues API:
    - Получение списка задач
    - Добавление комментариев к задачам
    """

    def __init__(self):
        """
        Инициализация клиента:
        - base: базовый URL для запросов к Issues данного репозитория
        - headers: заголовки с токеном авторизации и указанием версии API
        """
        self.base = f"https://api.github.com/repos/{SETTINGS.github_repo}"
        self.headers = {
            "Authorization": f"token {SETTINGS.github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def list_issues(self):
        """
        Получить список открытых issues репозитория.

        :return: список задач в формате JSON
        :raises: HTTPError, если запрос завершился с ошибкой
        """
        url = f"{self.base}/issues"
        # Отправляем GET-запрос к GitHub API
        resp = requests.get(url, headers=self.headers)
        # Выбрасываем исключение при статусе != 200
        resp.raise_for_status()
        # Возвращаем JSON-ответ (список issues)
        return resp.json()

    def comment_issue(self, issue_number: int, comment: str):
        """
        Добавить комментарий к указанному issue.

        :param issue_number: номер задачи в репозитории
        :param comment: текст комментария
        :return: JSON-ответ с данными созданного комментария
        :raises: HTTPError, если запрос завершился с ошибкой
        """
        url = f"{self.base}/issues/{issue_number}/comments"
        payload = {"body": comment}
        # Отправляем POST-запрос с телом комментария
        resp = requests.post(url, json=payload, headers=self.headers)
        # Выбрасываем исключение при ошибочном статусе
        resp.raise_for_status()
        # Возвращаем JSON-ответ (данные комментария)
        return resp.json()
