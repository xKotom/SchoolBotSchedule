from aiogram import types
from c_bot import bot, dp
from data_base import database
from aiogram.dispatcher import FSMContext
from handlers import states
from keyboards import usually_kb, inline_kb
from handlers.admin_side import add_proxy_data


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    all_users_id = [id_[0] for id_ in await database.get_all_users()]
    if message.from_user.id not in all_users_id:
        await database.add_user(message.from_user.id)
    await message.reply('Добро пожаловать в школьного бот!')
    
    keyboard = usually_kb.group_keyboard(await database.get_all_groups())
    keyboard.add(types.KeyboardButton('/help'))
    view_sche_kb = usually_kb.view_sche_kb()
    await bot.send_message(message.chat.id, 'Для просмотра рассписания ---> /view_schedule', reply_markup=view_sche_kb)

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    commands = [
        '/view_schedule - просмотр расписания',
        'Если у вас есть вопросы или проблемы пишите @G1sh1k'
    ]
    await message.reply('\n'.join(commands), reply=False)





# Просмотр рассписания 
@dp.message_handler(commands=['view_schedule'])
@dp.message_handler(text=['Просмотреть расписание'])
async def view_schedule_start(message: types.Message):
    all_groups = await database.get_all_groups()
    group_kb = usually_kb.group_keyboard(all_groups)
    await message.answer('Выберите группу(класс) для просмотра расписания', reply=False,
                        reply_markup=group_kb)
    await states.ViewScheduleStates.group_name.set()

@dp.message_handler(state=states.ViewScheduleStates.group_name)
async def view_schedule_group_state(message: types.Message, state: FSMContext):
    all_groups_names = [name[0] for name in await database.get_all_groups()]
    if message.text in all_groups_names:
        async with state.proxy() as data:
            data['group_name'] = message.text
        all_subgroups = await database.get_subgroups(message.text)
        subgroup_kb = usually_kb.subgroup_keyboard(all_subgroups)
        await message.answer('Выберите подгруппу(Букву класса) для просмотра расписания', reply=False,
                         reply_markup=subgroup_kb)
        await states.ViewScheduleStates.subgroup_name.set()
    elif message.text == "Выйти":
        await bot.send_message(message.chat.id, 'Выход из просмотра расписания')
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Класс(группа) которую вы хотите просмотреть расписание - не существует!')
        await state.finish()

@dp.message_handler(state=states.ViewScheduleStates.subgroup_name)
async def view_schedule_subgroup_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        group_name = data['group_name']
    all_subgroups_names = [name[0] for name in await database.get_subgroups(group_name)]
    if message.text in all_subgroups_names:
        async with state.proxy() as data:
            data['subgroup_name'] = message.text
        day_kb = await usually_kb.day_keyboard(message.text, group_name, database)
        await message.answer('Выберите день недели для просмотра расписания', reply=False,
                         reply_markup=day_kb)
        await states.ViewScheduleStates.day_name.set()
    elif message.text == "Выйти":
        await bot.send_message(message.chat.id, 'Выход из просмотра расписания')
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Подгруппа(буква) которую вы хотите просмотреть расписание - не существует!')
        await state.finish()

@dp.message_handler(state=states.ViewScheduleStates.day_name)
async def view_schedule_day_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        group_name = data['group_name']
        subgroup_name = data['subgroup_name']
        data['day_name'] = message.text  
    day_name = data['day_name']
    view_sche_kb = usually_kb.view_sche_kb()
    print(f"Группа: {group_name}, Буква: {subgroup_name}, День: {day_name}")
    print("Выходные данные от клиента:")
    print(f"SELECT * FROM schedules WHERE group_name = '{group_name}' AND subgroup_name = '{subgroup_name}' AND day_name = '{day_name}'")
    
    schedule_text = await database.get_schedule(group_name, subgroup_name, day_name)
    if schedule_text:
        await message.reply(f'Расписание для {group_name} "{subgroup_name}" на {day_name}:\n{schedule_text}', reply=False, reply_markup=view_sche_kb)
    else:
        await message.reply(f'Расписание для {group_name} "{subgroup_name}" на {day_name} не найдено', reply=False, reply_markup=view_sche_kb)
    await state.finish()