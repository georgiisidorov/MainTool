from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2


bot = Bot(token='token', parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(prefix='maintool')
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()

