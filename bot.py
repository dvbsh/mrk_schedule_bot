from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from config import bot_token


async def set_default_commands(bot_):
    await bot_.set_my_commands(
        commands=[
            BotCommand(command='sch', description='📚 Узнать расписание & "/расп", "/пара"'),
            BotCommand(command='follow', description='✅ Напоминание о начале пары'),
            BotCommand(command='unfollow', description='❌ Отключить напоминание')
        ],
        scope=BotCommandScopeDefault()
    )


bot = Bot(bot_token)
