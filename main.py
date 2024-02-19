import logging
import asyncio
from dispatcher import dp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import bot, set_default_commands
from tools.misc import warn


async def main():
    logging.basicConfig(level=logging.INFO)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(warn, 'cron', hour='19', minute='10', day_of_week='mon-fri')
    scheduler.start()
    await set_default_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
