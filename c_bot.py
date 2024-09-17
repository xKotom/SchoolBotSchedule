from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

storage = MemoryStorage()


bot = Bot(token="YOUR_BOT_TOKEN")
ADMINS_CHAT_ID = YOUR_ID

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())