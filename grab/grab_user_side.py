
# @dp.message_handler(state=states.StartStates.group_name)
# async def start_state(message: types.Message, state: FSMContext):
#     all_group_names = [_[0] for _ in await database.get_all_groups()]
#     if message.text in all_group_names:
#         await database.change_user_group(message.from_user.id, message.text)
#         await bot.send_message(message.chat.id, f'Окей, прикрепил тебя к группе {message.text}',
#                                reply_markup=types.ReplyKeyboardRemove())
#         await bot.send_message(message.chat.id, 'Выбери подгруппу',
#                                reply_markup=usually_kb.subgroup_keyboard(await database.get_subgroups(message.text)))
#         await states.StartStates.subgroup_name.set()
#     else:
#         await bot.send_message(message.chat.id, 'Ты пропустил выбор группу, но всегда сможешь'
#                                                 ' выбрать ее с помощью /select_group',
#                                reply_markup=types.ReplyKeyboardRemove())
#         await state.finish()


# @dp.message_handler(state=states.StartStates.subgroup_name)
# async def subgroup_state(message: types.Message, state: FSMContext):
#     group_name = (await database.get_only_such_users(message.from_user.id))[0][1]
#     subgroup_names = [_[0] for _ in await database.get_subgroups(group_name)]
#     if message.text in subgroup_names:
#         await bot.send_message(message.chat.id, f'Окей, прикрепил тебя к подгруппе {message.text}',
#                                reply_markup=types.ReplyKeyboardRemove())
#         await bot.send_message(message.chat.id, 'С помощью команды /view_group ты можешь посмотреть расписание',
#                                reply_markup=types.ReplyKeyboardRemove())
#         await state.finish()


# @dp.message_handler(state=states.StartStates.day_name)
# async def day_state(message: types.Message, state: FSMContext):
#     group_name = await database.get_only_such_users(message.from_user.id)[0][1]
#     subgroup_name = await database.get_only_such_users(message.from_user.id)[0][1]
#     day_names = [_[0] for _ in await database.get_days(subgroup_name, group_name)]
#     if message.text in day_names:
#         await bot.send_message(message.chat.id, f'Окей, прикрепил тебя к дню {message.text}',
#                                reply_markup=types.ReplyKeyboardRemove())
#     else:
#         await bot.send_message(message.chat.id, 'Ты пропустил выбор дня, но всегда сможешь'
#                                                 ' выбрать его с помощью /select_day',
#                                reply_markup=types.ReplyKeyboardRemove())
#     await state.finish()

    
# @dp.message_handler(commands=['news', 'новости'])
# async def news_command(message: types.Message):
#     news = await database.get_news()
#     for i in news[:3]:
#         await bot.send_photo(message.chat.id, i[3], f'*{i[1]}*\n\n{i[2]}',
#                              parse_mode='Markdown')


# @dp.message_handler(commands=['ask_question'])
# async def ask_question_command(message: types.Message):
#     await message.reply('Напишите свой вопрос', reply=False)
#     await states.AskQuestionStates.get_question.set()


# @dp.message_handler(state=states.AskQuestionStates.get_question)
# async def get_question_state(message: types.Message, state: FSMContext):
#     await add_proxy_data(state, {
#         'user_id': message.from_user.id,
#         'question': message.text,
#         'nick': message.from_user.username,
#     })
#     await database.add_question(state)
#     await message.reply('Вопрос задан, ждите ответа...', reply=False)














# @dp.message_handler(commands=['select_group'])
# async def select_group_command(message: types.Message):
#     all_groups = await database.get_all_groups()
#     group_kb = usually_kb.group_keyboard(all_groups)
#     await message.reply('Выбери группу', reply=False,
#                         reply_markup=group_kb)
#     await states.SelectGroupStates.group_name.set()
    
# @dp.message_handler(commands=['view_schedule'])
# async def view_schedule_command(message: types.Message):
#     await message.reply('Выберите группу', reply=False,
#                         reply_markup=usually_kb.group_keyboard(await database.get_all_groups()))
#     await states.ViewScheduleStates.group_name.set()

# @dp.message_handler(state=states.ViewScheduleStates.group_name)
# async def view_schedule_group_state(message: types.Message, state: FSMContext):
#     all_group_names = [_[0] for _ in await database.get_all_groups()]
#     if message.text in all_group_names:
#         async with state.proxy() as data:
#             data['group_name'] = message.text
#         await message.reply('Выберите подгруппу', reply=False,
#                             reply_markup=usually_kb.subgroup_keyboard(await database.get_subgroups(message.text)))
#         await states.ViewScheduleStates.subgroup_name.set()
#     else:
#         await bot.send_message(message.chat.id, 'Группу которую ты выбрал, не существует',
#                                reply_markup=types.ReplyKeyboardRemove())
#         await state.finish()

# @dp.message_handler(state=states.ViewScheduleStates.subgroup_name)
# async def view_schedule_subgroup_state(message: types.Message, state: FSMContext):
#     group_name = (await state.get_data()).get('group_name')
#     subgroup_names = [_[0] for _ in await database.get_subgroups(group_name)]
#     if message.text in subgroup_names:
#         async with state.proxy() as data:
#             data['subgroup_name'] = message.text
#         await message.reply('Выберите день недели', reply=False,
#                             reply_markup=usually_kb.day_keyboard(await database.get_days(message.text, group_name)))
#         await states.ViewScheduleStates.day_name.set()
#     else:
#         await bot.send_message(message.chat.id, 'Подгруппу которую ты выбрал, не существует',
#                                reply_markup=types.ReplyKeyboardRemove())
#         await state.finish()

# @dp.message_handler(state=states.ViewScheduleStates.day_name)
# async def view_schedule_day_state(message: types.Message, state: FSMContext):
#     group_name = (await state.get_data()).get('group_name')
#     subgroup_name = (await state.get_data()).get('subgroup_name')
#     day_names = [_[0] for _ in await database.get_days(subgroup_name, group_name)]
#     if message.text in day_names:
#         schedule = await database.get_schedule(subgroup_name, group_name, message.text)
#         if schedule:
#             await bot.send_message(message.chat.id, f"Расписание для {subgroup_name} ({group_name}) на {message.text}:\n{schedule}")
#         else:
#             await bot.send_message(message.chat.id, f"Расписание для {subgroup_name} ({group_name}) на {message.text} не найдено")
#         await state.finish()
#     else:
#         await bot.send_message(message.chat.id, 'День недели который ты выбрал, не существует',
#                                reply_markup=types.ReplyKeyboardRemove())
#         await state.finish()

# @dp.message_handler(state=states.ViewScheduleStates.group_name, text='Назад')
# async def view_schedule_back_to_group(message: types.Message, state: FSMContext):
#     await message.reply('Выберите группу', reply=False,
#                         reply_markup=usually_kb.group_keyboard(await database.get_all_groups()))
#     await states.ViewScheduleStates.group_name.set()

# @dp.message_handler(state=states.ViewScheduleStates.subgroup_name, text='Назад')
# async def view_schedule_back_to_subgroup(message: types.Message, state: FSMContext):
#     group_name = (await state.get_data()).get('group_name')
#     await message.reply('Выберите подгруппу', reply=False,
#                         reply_markup=usually_kb.subgroup_keyboard(await database.get_subgroups(group_name)))
#     await states.ViewScheduleStates.subgroup_name.set()

# @dp.message_handler(state=states.ViewScheduleStates.day_name, text='Назад')
# async def view_schedule_back_to_day(message: types.Message, state: FSMContext):
#     group_name = (await state.get_data()).get('group_name')
#     subgroup_name = (await state.get_data()).get('subgroup_name')
#     await message.reply('Выберите день недели', reply=False,
#                         reply_markup=usually_kb.day_keyboard(await database.get_days(subgroup_name, group_name)))
#     await states.ViewScheduleStates.day_name.set()

# @dp.message_handler(state=states.SelectGroupStates.group_name)
# async def select_group_state(message: types.Message, state: FSMContext):
#     all_group_names = [_[0] for _ in await database.get_all_groups()]
#     if message.text in all_group_names:
#         await database.change_user_group(message.from_user.id, message.text)
#         await bot.send_message(message.chat.id,
#                                reply_markup=types.ReplyKeyboardRemove())
#         await bot.send_message(message.chat.id, 'Выбери подгруппу',
#                                reply_markup=usually_kb.subgroup_keyboard(await database.get_subgroups(message.text)))
#         await states.SelectGroupStates.subgroup_name.set()
#     else:
#         await bot.send_message(message.chat.id, 'Группу которую ты выбрал, не существует',
#                                reply_markup=types.ReplyKeyboardRemove())
#         await state.finish()


# @dp.message_handler(state=states.SelectGroupStates.subgroup_name)
# async def select_subgroup_state(message: types.Message, state: FSMContext):
#     group_name = (await database.get_only_such_users(message.from_user.id))[0][1]
#     subgroup_names = [_[0] for _ in await database.get_subgroups(group_name)]
#     if message.text in subgroup_names:
#         await database.change_user_subgroup(message.from_user.id, message.text)
#         await bot.send_message(message.chat.id, f'Окей, прикрепил тебя к подгруппе {message.text}',
#                                reply_markup=types.ReplyKeyboardRemove())
#         await bot.send_message(message.chat.id, 'Выбери день недели',
#                                reply_markup=usually_kb.day_keyboard(await database.get_days(message.text, group_name)))
#         await states.SelectGroupStates.day_name.set()
#     else:
#         await bot.send_message(message.chat.id, 'Ты пропустил выбор подгруппы, но всегда сможешь'
#                                                 ' выбрать ее с помощью /select_subgroup',
#                                reply_markup=types.ReplyKeyboardRemove())
#         await state.finish()

# @dp.message_handler(state=states.SelectGroupStates.day_name)
# async def select_day_state(message: types.Message, state: FSMContext):
#     group_name = (await database.get_only_such_users(message.from_user.id))[0][1]
#     subgroup_name = (await database.get_only_such_users(message.from_user.id))[0][2]
#     day_names = [_[0] for _ in await database.get_days(subgroup_name, group_name)]
#     if message.text in day_names:
#         await state.update_data(day_name=message.text)
#         await bot.send_message(message.chat.id, f'Окей, выбран день {message.text}',
#                                reply_markup=types.ReplyKeyboardRemove())
#         await bot.send_message(message.chat.id, 'Выбери расписание',
#                                reply_markup=usually_kb.schedule_keyboard(await database.get_schedules(subgroup_name, group_name, message.text)))
#         await states.CreateScheduleStates.schedule_text.set()
#     else:
#         await bot.send_message(message.chat.id, 'Ты пропустил выбор дня, но всегда сможешь'
#                                                 ' выбрать его с помощью /select_day',
#                                reply_markup=types.ReplyKeyboardRemove())
#         await state.finish()


# @dp.message_handler(state=states.CreateScheduleStates.subgroup_name)
# async def create_schedule_subgroup_state(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         group_name = data['group_name']
#     all_subgroups_names = [name[0] for name in await database.get_subgroups(group_name)]
#     if message.text in all_subgroups_names:
#         async with state.proxy() as data:
#             data['subgroup_name'] = message.text
#         day_kb = usually_kb.day_keyboard(message.text, group_name, database)
#         await message.answer('Выберите день недели для создания расписания', reply=False,
#                          reply_markup=day_kb)
#         await states.CreateScheduleStates.day_name.set()
#     elif message.text == "Выйти":
#         await bot.send_message(message.chat.id, 'Выход из создания расписания')
#         await state.finish()
#     else:
#         await bot.send_message(message.chat.id, 'Подгруппа которую вы хотите создать расписание - не существует!')
#         await state.finish()

# @dp.message_handler(commands=['id'])
# async def get_group_id(message: types.Message, state: FSMContext):
#     await message.reply(message.chat.id,)
