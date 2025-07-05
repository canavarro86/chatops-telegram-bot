# bot/handlers/commands.py

import requests
from aiogram import types
from aiogram.filters import Command
from config.config import SETTINGS
from bot.services.github_api import GitHubAPI
from bot.services.ci_api import CIAPI

def register_handlers(dp, verify_jwt):
    gh = GitHubAPI()
    ci = CIAPI()

    @dp.message(Command("issues"))
    async def cmd_issues(message: types.Message):
        user = verify_jwt(message.text)
        if not user:
            return await message.reply("❌ Неверный токен.")
        issues = gh.list_issues(SETTINGS.github_repo)
        text = "\n".join(f"- #{i['number']} {i['title']}" for i in issues)
        await message.reply(f"Открытые задачи:\n{text}")

    @dp.message(lambda m: m.text and m.text.startswith("/build "))
    async def cmd_build(message: types.Message):
        parts = message.text.split(maxsplit=1)
        workflow_id = parts[1]
        result = ci.trigger_build(workflow_id)
        await message.reply(f"Запуск сборки `{workflow_id}`: {result}")

    @dp.message(Command("workflows"))
    async def cmd_workflows(message: types.Message):
        """
        Выводит список всех GitHub Actions workflows и их ID.
        """
        url = f"https://api.github.com/repos/{SETTINGS.github_repo}/actions/workflows"
        resp = requests.get(url, headers=gh.headers)
        resp.raise_for_status()
        data = resp.json().get("workflows", [])
        if not data:
            return await message.reply("Workflows не найдены.")
        lines = [
            f"- id: {w['id']}, name: {w['name']}, path: {w['path']}"
            for w in data
        ]
        await message.reply("Доступные workflows:\n" + "\n".join(lines))
        
    @dp.message(Command("status"))
    async def cmd_status(message: types.Message):
        parts = message.text.split(maxsplit=1)
        wf_id = parts[1] if len(parts) > 1 else None
        if not wf_id:
            return await message.reply("Укажите ID workflow: /status <id>")
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

