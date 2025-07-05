import requests
from aiogram import types
from aiogram.filters import Command
from config.config import SETTINGS
from bot.services.github_api import GitHubAPI
from bot.services.ci_api import CIAPI
from requests.exceptions import HTTPError

def register_handlers(dp, verify_jwt):
    gh = GitHubAPI()
    ci = CIAPI()

    # Открытая команда: просто выдаёт список issues
    @dp.message(Command("issues"))
    async def cmd_issues(message: types.Message):
        issues = gh.list_issues()
        if not issues:
            return await message.reply("Задач не найдено.")
        text = "\n".join(f"- #{i['number']} {i['title']}" for i in issues)
        await message.reply(f"Открытые задачи:\n{text}")

    # /comment требует JWT
    @dp.message(lambda m: m.text and m.text.startswith("/comment "))
    async def cmd_comment(message: types.Message):
        # формат: /comment <jwt> <issue_number> <текст>
        parts = message.text.split(maxsplit=3)
        if len(parts) < 4:
            return await message.reply("Использование: /comment <токен> <номер> <текст>")
        token, issue_str, comment = parts[1], parts[2], parts[3]
        if not verify_jwt(token):
            return await message.reply("❌ Неверный токен.")
        try:
            num = int(issue_str)
        except ValueError:
            return await message.reply("Номер issue должен быть числом.")
        try:
            resp = gh.comment_issue(num, comment)
        except HTTPError as e:
            if e.response.status_code == 404:
                return await message.reply(f"Issue #{num} не найден.")
            raise
        url = resp.get("html_url") or resp.get("url")
        await message.reply(f"Коммент добавлен: {url}")

    # /build требует JWT
    @dp.message(lambda m: m.text and m.text.startswith("/build "))
    async def cmd_build(message: types.Message):
        # формат: /build <токен> <workflow_id>
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            return await message.reply("Использование: /build <токен> <workflow_id>")
        token, workflow_id = parts[1], parts[2]
        if not verify_jwt(token):
            return await message.reply("❌ Неверный токен.")
        result = ci.trigger_build(workflow_id)
        await message.reply(f"Запуск сборки `{workflow_id}`: {result}")

    @dp.message(Command("workflows"))
    async def cmd_workflows(message: types.Message):
        url = f"https://api.github.com/repos/{SETTINGS.github_repo}/actions/workflows"
        resp = requests.get(url, headers=gh.headers)
        resp.raise_for_status()
        data = resp.json().get("workflows", [])
        if not data:
            return await message.reply("Workflows не найдены.")
        lines = [f"- id: {w['id']}, name: {w['name']}, path: {w['path']}" for w in data]
        await message.reply("Доступные workflows:\n" + "\n".join(lines))

    # /status требует JWT
    @dp.message(Command("status"))
    async def cmd_status(message: types.Message):
        # формат: /status <токен> <workflow_id>
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            return await message.reply("Использование: /status <токен> <workflow_id>")
        token, wf_id = parts[1], parts[2]
        if not verify_jwt(token):
            return await message.reply("❌ Неверный токен.")
        status = ci.get_last_run(wf_id)
        if not status:
            return await message.reply("Запусков не найдено.")
        text = (
            f"Последний запуск workflow {wf_id}:\n"
            f"- Run ID: {status['id']}\n"
            f"- Status: {status['status']}\n"
            f"- Conclusion: {status.get('conclusion')}"
        )
        await message.reply(text)
