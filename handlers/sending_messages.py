from c_bot import bot
from data_base import database


async def sending_schedule(name):
    users = await database.get_only_such_users(name)
    group = await database.get_group(name)
    for user in users:
        await bot.send_photo(user[0], group[0][1], caption='РАСПИСАНИЕ ВАШЕЙ ГРУППЫ ОБНОВЛЕНО')
