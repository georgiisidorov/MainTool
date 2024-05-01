from aiogram import executor

from handlers import dp
from loader import bot, storage, scheduler
import middlewares as middlewares
from utils.db_api import db_gino, quick_commands
from handlers.users.maintool_spider import services_getter


async def update_services():
    services = services_getter()

    min_avg_time_subs = min([services['6685'], services['7110']])
    min_avg_time_views = min([services['6583'], services['1365']])

    for k, v in services.items():
        if v == min_avg_time_views:
            await quick_commands.update_settings('views', k)
        elif v == min_avg_time_subs:
            await quick_commands.update_settings('subs', k)


def update_service_ids():
    scheduler.add_job(update_services, "interval", seconds=600)


async def on_startup(dp):
    await db_gino.on_startup(dp)
    update_service_ids()
    await quick_commands.add_settings(1, 'subs', '6685')
    await quick_commands.add_settings(2, 'views', '1365')
    # await dp.storage.reset_all()
    middlewares.setup(dp)


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)