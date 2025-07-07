import requests
from aiogram import types
from aiogram.filters import Command
from config.config import SETTINGS
from bot.services.github_api import GitHubAPI
from bot.services.ci_api import CIAPI
from requests.exceptions import HTTPError


def register_handlers(dp, verify_jwt):
    """
    Регистрирует обработчики команд Telegram-бота.

    :param dp: Dispatcher из aiogram
    :param verify_jwt: функция для проверки JWT-токена
    """
    # Создаём экземпляры клиентов для GitHub и CI
    gh = GitHubAPI()
    ci = CIAPI()

    @dp.message(Command("issues"))
    async def cmd_issues(message: types.Message):
        """
        Обработчик команды /issues:
        получает список открытых задач из GitHub и отправляет их в чат.
        """
        issues = gh.list_issues()
        if not issues:
            # Если задач нет — уведомляем пользователя
            return await message.reply("Задач не найдено.")

        # Формируем текст ответа
        text = "\n".join(f"- #{i['number']} {i['title']}" for i in issues)
        await message.reply(f"Открытые задачи:\n{text}")

    @dp.message(lambda m: m.text and m.text.startswith("/comment "))
    async def cmd_comment(message: types.Message):
        """
        Обработчик команды /comment <jwt> <номер> <текст>:
        проверяет токен, номер задачи и добавляет комментарий.
        """
        # Разбиваем текст на части: команда, токен, номер, текст комментария
        parts = message.text.split(maxsplit=3)
        if len(parts) < 4:
            return await message.reply("Использование: /comment <токен> <номер> <текст>")

        token, issue_str, comment = parts[1], parts[2], parts[3]

        # Проверяем JWT-токен
        if not verify_jwt(token):
            return await message.reply("❌ Неверный токен.")

        # Преобразуем номер задачи в int
        try:
            num = int(issue_str)
        except ValueError:
            return await message.reply("Номер issue должен быть числом.")

        # Пытаемся добавить комментарий
        try:
            resp = gh.comment_issue(num, comment)
        except HTTPError as e:
            # Если issue не найден — сообщаем об этом
            if e.response.status_code == 404:
                return await message.reply(f"Issue #{num} не найден.")
            # Иначе пробрасываем исключение
            raise

        # Получаем URL созданного комментария
        url = resp.get("html_url") or resp.get("url")
        await message.reply(f"Коммент добавлен: {url}")

    @dp.message(lambda m: m.text and m.text.startswith("/build "))
    async def cmd_build(message: types.Message):
        """
        Обработчик команды /build <jwt> <workflow_id>:
        проверяет токен и запускает указанную сборку CI/CD.
        """
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            return await message.reply("Использование: /build <токен> <workflow_id>")

        token, workflow_id = parts[1], parts[2]

        # Проверяем JWT-токен
        if not verify_jwt(token):
            return await message.reply("❌ Неверный токен.")

        # Запускаем сборку через CIAPI
        result = ci.trigger_build(workflow_id)
        await message.reply(f"Запуск сборки `{workflow_id}`: {result}")

    @dp.message(Command("workflows"))
    async def cmd_workflows(message: types.Message):
        """
        Обработчик команды /workflows:
        запрашивает список CI/CD workflows и отправляет их в чат.
        """
        # Формируем URL и делаем HTTP-запрос
        url = f"https://api.github.com/repos/{SETTINGS.github_repo}/actions/workflows"
        resp = requests.get(url, headers=gh.headers)
        resp.raise_for_status()

        data = resp.json().get("workflows", [])
        if not data:
            return await message.reply("Workflows не найдены.")

        # Формируем список строк с информацией о workflow
        lines = [
            f"- id: {w['id']}, name: {w['name']}, path: {w['path']}"
            for w in data
        ]
        await message.reply("Доступные workflows:\n" + "\n".join(lines))

    @dp.message(Command("status"))
    async def cmd_status(message: types.Message):
        """
        Обработчик команды /status <jwt> <workflow_id>:
        проверяет токен и показывает статус последнего запуска workflow.
        """
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            return await message.reply("Использование: /status <токен> <workflow_id>")

        token, wf_id = parts[1], parts[2]

        # Проверяем JWT-токен
        if not verify_jwt(token):
            return await message.reply("❌ Неверный токен.")

        status = ci.get_last_run(wf_id)
        if not status:
            return await message.reply("Запусков не найдено.")

        # Формируем текст с деталями последнего запуска
        text = (
            f"Последний запуск workflow {wf_id}:\n"
            f"- Run ID: {status['id']}\n"
            f"- Status: {status['status']}\n"
            f"- Conclusion: {status.get('conclusion')}"
        )
        await message.reply(text)
