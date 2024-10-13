from c_bot import bot, dp 
from aiogram.utils  import executor
from data_base import database as db
from handlers import admin_side, user_side


async def on_startup(_):
     db.sql_start()
     print('Бот успешно подключен к базе данных')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)  

