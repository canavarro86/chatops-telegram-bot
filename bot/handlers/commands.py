# bot/handlers/commands.py
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
        workflow = parts[1]  # e.g. "ci.yml" или ID
        result = ci.trigger_build(workflow)  # передаём только workflow_id
        await message.reply(f"Запуск сборки `{workflow}`: {result}")
