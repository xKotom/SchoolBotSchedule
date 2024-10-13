from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from keyboards import usually_kb
from c_bot import bot, dp, ADMINS_CHAT_ID
from handlers import states
from keyboards import inline_kb
from handlers import sending_messages
from data_base import database
from data_base.database import get_data_from_proxy


async def add_proxy_data(state, data: dict):
    async with state.proxy() as proxy:
        for k,v in data.items():
            proxy[k] = v


        
@dp.message_handler(commands=['cmd'])
async def help_command(message: types.Message):
    if message.from_user.id == ADMINS_CHAT_ID:
        cmd_kb = usually_kb.cmd_kb()
        commands = [
            '/create_group - Создать группу ✅',
            '/delete_group - Удалить группу ❌',
            '/create_subgroup - Создать подгруппу ✅',
            '/delete_subgroup - Удалить подгруппу ❌',
            '/create_schedule - Создать расписание ✅',
            '/delete_schedule - Удалить расписание ❌',
            '/view_schedule - Просмотр расписания 👀'
        ]
        await message.reply('\n'.join(commands), reply=False,)
        await message.reply('Административные команды:', reply=False, reply_markup=cmd_kb)

@dp.message_handler(commands=['my_command'])
async def my_command(message: types.Message):
    if message.from_user.id == ADMINS_CHAT_ID:
        await message.reply('You are an admin!')

@dp.message_handler(commands=['my_command'])
async def my_command(message: types.Message):
    await message.reply('Мечтай об adminke!')


# ------------- Группа -------------
# Создание
@dp.message_handler(commands=['create_group'])
@dp.message_handler(text=['Создать группу ✅'])
async def create_group_command(message: types.Message):
    if message.from_user.id == ADMINS_CHAT_ID:
        await message.reply('Введите название группы')
        await states.CreateGroupStates.group_name.set()


@dp.message_handler(state=states.CreateGroupStates.group_name)
async def create_group_state(message: types.Message, state: FSMContext):
    await database.add_group(message.text, message)
    await message.reply('Группа создана!', reply=False)
    await state.finish()

#Удаление 
@dp.message_handler(commands=['delete_group'])
@dp.message_handler(text=['Удалить группу ❌'])
async def delete_group_command(message: types.Message):
    if message.from_user.id == ADMINS_CHAT_ID:
        all_groups = await database.get_all_groups()
        group_kb = usually_kb.group_keyboard(all_groups)
        await message.answer('Выберите группу для удаления', reply=False,
                         reply_markup=group_kb)
        await states.DeleteGroupStates.group_name.set()


@dp.message_handler(state=states.DeleteGroupStates.group_name)
async def delete_group_state(message: types.Message, state: FSMContext):
    all_groups_names = [name[0] for name in await database.get_all_groups()]
    if message.text in all_groups_names:
        await database.delete_group(message.text)
        await message.reply('Группа удалена!', reply=False,
                            reply_markup=types.ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, 'Группа которую вы хотите удалить - не существует!')
    await state.finish()

# ------------- Подгруппа -------------
# Создание 
@dp.message_handler(commands=['create_subgroup'])
@dp.message_handler(text=['Создать подгруппу ✅'])
async def create_subgroup_command(message: types.Message):
    if message.from_user.id == ADMINS_CHAT_ID:
        all_groups = await database.get_all_groups()
        group_kb = usually_kb.group_keyboard(all_groups)
        await message.answer('Выберите группу для создания подгруппы', reply=False,
                         reply_markup=group_kb)
        await states.CreateSubgroupStates.group_name.set()

@dp.message_handler(state=states.CreateSubgroupStates.group_name)
async def create_subgroup_group_state(message: types.Message, state: FSMContext):
    all_groups_names = [name[0] for name in await database.get_all_groups()]
    if message.text in all_groups_names:
        async with state.proxy() as data:
            data['group_name'] = message.text
        await message.reply('Введите название подгруппы')
        await states.CreateSubgroupStates.subgroup_name.set()
    else:
        await bot.send_message(message.chat.id, 'Группа которую вы хотите создать подгруппу - не существует!')
        await state.finish()


@dp.message_handler(state=states.CreateSubgroupStates.subgroup_name)
async def create_subgroup_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        group_name = data['group_name']
    await database.create_subgroup(group_name, message.text, message)
    await message.reply('Подгруппа создана!', reply=False)
    await state.finish()


# Удаление
@dp.message_handler(commands=['delete_subgroup'])
@dp.message_handler(text=['Удалить подгруппу ❌'])
async def delete_subgroup_command(message: types.Message):
    if message.from_user.id == ADMINS_CHAT_ID:
        all_groups = await database.get_all_groups()
        group_kb = usually_kb.group_keyboard(all_groups)
        await message.answer('Выберите группу для удаления подгруппы', reply=False,
                         reply_markup=group_kb)
        await states.DeleteSubgroupStates.group_name.set()

@dp.message_handler(state=states.DeleteSubgroupStates.group_name)
async def delete_subgroup_group_state(message: types.Message, state: FSMContext):
    all_groups_names = [name[0] for name in await database.get_all_groups()]
    if message.text in all_groups_names:
        async with state.proxy() as data:
            data['group_name'] = message.text
        all_subgroups = await database.get_subgroups(message.text)
        subgroup_kb = usually_kb.group_keyboard(all_subgroups)
        await message.reply('Выберите подгруппу для удаления', reply=False,
                         reply_markup=subgroup_kb)
        await states.DeleteSubgroupStates.subgroup_name.set()
    else:
        await bot.send_message(message.chat.id, 'Группа которую вы хотите удалить подгруппу - не существует!')
        await state.finish()

@dp.message_handler(state=states.DeleteSubgroupStates.subgroup_name)
async def delete_subgroup_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        group_name = data['group_name']
    await database.delete_subgroup(group_name, message.text)
    await message.reply('Подгруппа удалена!', reply=False)
    await state.finish()




# ------------- Рассписания -------------
# Создание
@dp.message_handler(commands=['create_schedule'])
@dp.message_handler(text=['Создать расписание ✅'])
async def create_schedule_start(message: types.Message):
    if message.from_user.id == ADMINS_CHAT_ID:
        all_groups = await database.get_all_groups()
        group_kb = usually_kb.group_keyboard(all_groups)
        await message.answer('Выберите группу для создания расписания', reply=False,
                         reply_markup=group_kb)
        await states.CreateScheduleStates.group_name.set()

@dp.message_handler(state=states.CreateScheduleStates.group_name)
async def create_schedule_group_state(message: types.Message, state: FSMContext):
    all_groups_names = [name[0] for name in await database.get_all_groups()]
    if message.text in all_groups_names:
        async with state.proxy() as data:
            data['group_name'] = message.text
        all_subgroups = await database.get_subgroups(message.text)
        subgroup_kb = usually_kb.subgroup_keyboard(all_subgroups)
        await message.answer('Выберите подгруппу для создания расписания', reply=False,
                         reply_markup=subgroup_kb)
        await states.CreateScheduleStates.subgroup_name.set()
    elif message.text == "Выйти":
        await bot.send_message(message.chat.id, 'Выход из создания расписания')
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Группа которую вы хотите создать расписание - не существует!')
        await state.finish()

@dp.message_handler(state=states.CreateScheduleStates.subgroup_name)
async def create_schedule_subgroup_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        group_name = data['group_name']
    all_subgroups_names = [name[0] for name in await database.get_subgroups(group_name)]
    if message.text in all_subgroups_names:
        async with state.proxy() as data:
            data['subgroup_name'] = message.text
        day_kb = await usually_kb.day_keyboard(message.text, group_name, database)
        await message.answer('Выберите день недели для создания расписания', reply=False,
                         reply_markup=day_kb)
        await states.CreateScheduleStates.day_name.set()
    elif message.text == "Выйти":
        await bot.send_message(message.chat.id, 'Выход из создания расписания')
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Подгруппа которую вы хотите создать расписание - не существует!')
        await state.finish()

@dp.message_handler(state=states.CreateScheduleStates.day_name)
async def select_day_state(message: types.Message, state: FSMContext):
    day_name = message.text
    async with state.proxy() as data:
        data['day_name'] = day_name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Выйти")
    markup.add("Продолжить")
    await message.reply('Введите расписание (например, 1  08:00 - 08:40  Русский язык/2  08:50 - 09:30  Алгебра):', reply_markup=markup)
    await states.CreateScheduleStates.schedule_text.set()

@dp.message_handler(state=states.CreateScheduleStates.schedule_text)
async def create_schedule_state(message: types.Message, state: FSMContext):
    if message.text == "Выйти":
        await bot.send_message(message.chat.id, 'Выход из создания расписания')
        await state.finish()
    else:
        async with state.proxy() as data:
            group_name = data['group_name']
            subgroup_name = data['subgroup_name']
            day_name = data['day_name']
            schedule_text = message.text
        await database.create_schedule(state, day_name, subgroup_name, group_name, schedule_text)
        await message.reply('Расписание добавлено!', reply=False)
        await state.finish()

# Удаление 
@dp.message_handler(commands=['delete_schedule'])
@dp.message_handler(text=['Удалить расписание ❌'])
async def delete_schedule_start(message: types.Message):
    if message.from_user.id == ADMINS_CHAT_ID:
        all_groups = await database.get_all_groups()
        group_kb = usually_kb.group_keyboard(all_groups)
        await message.answer('Выберите группу для удаления расписания', reply=False,
                         reply_markup=group_kb)
        await states.DeleteScheduleStates.group_name.set()

@dp.message_handler(state=states.DeleteScheduleStates.group_name)
async def delete_schedule_group_state(message: types.Message, state: FSMContext):
    all_groups_names = [name[0] for name in await database.get_all_groups()]
    if message.text in all_groups_names:
        async with state.proxy() as data:
            data['group_name'] = message.text
        all_subgroups = await database.get_subgroups(message.text)
        subgroup_kb = usually_kb.subgroup_keyboard(all_subgroups)
        await message.answer('Выберите подгруппу для удаления расписания', reply=False,
                         reply_markup=subgroup_kb)
        await states.DeleteScheduleStates.subgroup_name.set()
    elif message.text == "Выйти":
        await bot.send_message(message.chat.id, 'Выход из удаления расписания')
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Группа которую вы хотите удалить расписание - не существует!')
        await state.finish()

@dp.message_handler(state=states.DeleteScheduleStates.subgroup_name)
async def delete_schedule_subgroup_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        group_name = data['group_name']
    all_subgroups_names = [name[0] for name in await database.get_subgroups(group_name)]
    if message.text in all_subgroups_names:
        async with state.proxy() as data:
            data['subgroup_name'] = message.text
        day_kb = await usually_kb.day_keyboard(message.text, group_name, database)
        await message.answer('Выберите день недели для удаления расписания', reply=False,
                         reply_markup=day_kb)
        await states.DeleteScheduleStates.day_name.set()
    elif message.text == "Выйти":
        await bot.send_message(message.chat.id, 'Выход из удаления расписания')
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Подгруппа которую вы хотите удалить расписание - не существует!')
        await state.finish()

@dp.message_handler(state=states.DeleteScheduleStates.day_name)
async def delete_schedule_day_state(message: types.Message, state: FSMContext):
    day_name = message.text
    async with state.proxy() as data:
        data['day_name'] = day_name
    async with state.proxy() as data:
        group_name = data['group_name']
        subgroup_name = data['subgroup_name']
        day_name = data['day_name']
    await database.delete_schedule(group_name, subgroup_name, day_name)
    await message.reply('Расписание удалено!', reply=False)
    print(data)
    await state.finish()