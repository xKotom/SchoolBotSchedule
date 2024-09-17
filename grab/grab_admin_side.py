admin side 

# @dp.message_handler(commands=['my_command'])
# async def my_command(message: types.Message):
#     if message.from_user.id == ADMINS_CHAT_ID:
#         await message.reply('You are an admin!')
#     else:
#         await message.reply('Мечтай об adminke!')


# @dp.message_handler(commands=['create_subgroup'])
# async def create_subgroup_command(message: types.Message):
#     if message.from_user.id == ADMINS_CHAT_ID:
#         all_groups = await database.get_all_groups()
#         group_kb = usually_kb.group_keyboard(all_groups)
#         await message.answer('Выберите группу для создания подгруппы', reply=False,
#                          reply_markup=group_kb)
#         await states.CreateSubgroupStates.group_name.set()

# @dp.message_handler(state=states.CreateSubgroupStates.group_name)
# async def create_subgroup_group_state(message: types.Message, state: FSMContext):
#     all_groups_names = [name[0] for name in await database.get_all_groups()]
#     if message.text in all_groups_names:
#         async with state.proxy() as data:
#             data['group_name'] = message.text
#         await message.reply('Введите название подгруппы')
#         await states.CreateSubgroupStates.subgroup_name.set()
#     else:
#         await bot.send_message(message.chat.id, 'Группа которую вы хотите создать подгруппу - не существует!')
#         await state.finish()

# @dp.message_handler(state=states.CreateSubgroupStates.subgroup_name)
# async def create_subgroup_state(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         group_name = data['group_name']
#     await database.add_subgroup(group_name, message.text, message)
#     await message.reply('Подгруппа создана!', reply=False)
#     await state.finish()


# @dp.message_handler(commands=['create_days'])
# async def create_days_command(message: types.Message):
#     all_groups = await database.get_all_groups()
#     group_kb = usually_kb.group_keyboard(all_groups)
#     await message.answer('Выберите группу для создания дней недели', reply=False,
#                          reply_markup=group_kb)
#     await states.CreateDayStates.group_name.set()

# @dp.message_handler(state=states.CreateDayStates.group_name)
# async def create_days_group_state(message: types.Message, state: FSMContext):
#     all_groups_names = [name[0] for name in await database.get_all_groups()]
#     if message.text in all_groups_names:
#         async with state.proxy() as data:
#             data['group_name'] = message.text
#         all_subgroups = await database.get_subgroups(message.text)
#         subgroup_kb = usually_kb.group_keyboard(all_subgroups)
#         await message.answer('Выберите подгруппу для создания дней недели', reply=False,
#                              reply_markup=subgroup_kb)
#         await states.CreateDayStates.subgroup_name.set()
#     else:
#         await bot.send_message(message.chat.id, 'Группа которую вы хотите создать дни недели - не существует!')
#         await state.finish()

# @dp.message_handler(state=states.CreateDayStates.subgroup_name)
# async def create_days_subgroup_state(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         group_name = data['group_name']
#         subgroup_name = message.text
#     await message.reply('Введите дни недели (через запятую):')
#     await states.CreateDayStates.days_name.set()

# @dp.message_handler(state=states.CreateDayStates.days_name)
# async def create_days(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         group_name = data['group_name']
#         subgroup_name = data['subgroup_name']  
#     days = message.text.split(',')
#     for day in days:
#         await database.add_day(subgroup_name, group_name, day, message)
#     await message.reply('Дни недели добавлены!')
#     await state.finish()


# @dp.message_handler(commands=['delete_days'])
# async def delete_days_command(message: types.Message):
#     all_groups = await database.get_all_groups()
#     group_kb = usually_kb.group_keyboard(all_groups)
#     await message.answer('Выберите группу для удаления дней недели', reply=False,
#                          reply_markup=group_kb)
#     await states.DeleteDayStates.group_name.set()

# @dp.message_handler(state=states.DeleteDayStates.group_name)
# async def delete_days_group_state(message: types.Message, state: FSMContext):
#     all_groups_names = [name[0] for name in await database.get_all_groups()]
#     if message.text in all_groups_names:
#         async with state.proxy() as data:
#             data['group_name'] = message.text
#         all_subgroups = await database.get_subgroups(message.text)
#         subgroup_kb = usually_kb.group_keyboard(all_subgroups)
#         await message.answer('Выберите подгруппу для удаления дней недели', reply=False,
#                              reply_markup=subgroup_kb)
#         await states.DeleteDayStates.subgroup_name.set()
#     else:
#         await bot.send_message(message.chat.id, 'Группа которую вы хотите удалить дни недели - не существует!')
#         await state.finish()

# @dp.message_handler(state=states.DeleteDayStates.subgroup_name)
# async def delete_days_subgroup_state(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         group_name = data['group_name']
#         subgroup_name = message.text
#     await message.reply('Введите дни недели для удаления (через запятую):')
#     await states.DeleteDayStates.days_name.set()
# @dp.message_handler(state=states.DeleteDayStates.days_name)
# async def delete_days(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         group_name = data['group_name']
#         subgroup_name = data['subgroup_name']
#     days = message.text.split(',')
#     for day in days:
#         try:
#             database.cursor.execute('DELETE FROM days WHERE subgroup_name = ? AND subgroup_group_name = ? AND day = ?', (subgroup_name, group_name, day))
#             database.conn.commit()
#         except:
#             await message.reply(f'День недели {day} не существует!')
#     await message.reply('Дни недели удалены!')
#     await state.finish()

# #days

# @dp.message_handler(commands=['create_day'])
# async def create_day_command(message: types.Message):
#     if message.from_user.id == ADMINS_CHAT_ID:
#         all_subgroups = await database.get_subgroups()
#         subgroup_kb = usually_kb.subgroup_keyboard(all_subgroups)
#         await message.answer('Выберите подгруппу для создания дня', reply=False,
#                          reply_markup=subgroup_kb)
#         await states.CreateDayStates.subgroup_name.set()

# @dp.message_handler(commands=['delete_day'])
# async def delete_day_command(message: types.Message):
#     if message.from_user.id == ADMINS_CHAT_ID:
#         all_days = await database.get_days()
#         day_kb = usually_kb.day_keyboard(all_days)
#         await message.answer('Выберите день для удаления', reply=False,
#                          reply_markup=day_kb)
#         await states.DeleteDayStates.day_name.set()


# # schedule
# @dp.message_handler(commands=['create_schedule'])
# async def create_schedule_command(message: types.Message):
#     if message.from_user.id == ADMINS_CHAT_ID:
#         all_days = await database.get_days()
#         day_kb = usually_kb.day_keyboard(all_days)
#         await message.answer('Выберите день для создания расписания', reply=False,
#                          reply_markup=day_kb)
#         await states.CreateScheduleStates.day_name.set()

# @dp.message_handler(commands=['delete_schedule'])
# async def delete_schedule_command(message: types.Message):
#     if message.from_user.id == ADMINS_CHAT_ID:
#         all_days = await database.get_days()
#         day_kb = usually_kb.day_keyboard(all_days)
#         await message.answer('Выберите день для удаления расписания', reply=False,
#                          reply_markup=day_kb)
#         await states.DeleteScheduleStates.day_name.set()


# @dp.message_handler(commands=['create_schedule'])
# async def create_schedule(message: types.Message):
#     if message.from_user.id == ADMINS_CHAT_ID:
#         groups = await database.get_all_groups()
#         await states.ScheduleStates.select_group.set()
#         await message.reply('Выберите группу, которой хотите обновить расписание', reply=False,
#                             reply_markup=usually_kb.group_keyboard(groups))


# @dp.message_handler(state=states.ScheduleStates.select_group)
# async def state_select_group_schedule(message: types.Message, state: FSMContext):
#     all_groups_names = [name[0] for name in await database.get_all_groups()]
#     if message.text in all_groups_names:
#         await add_proxy_data(state, {'group': message.text})
#         subgroups = await database.get_subgroups(message.text)
#         await states.ScheduleStates.select_subgroup.set()
#         await message.reply('Выберите подгруппу, которой хотите обновить расписание', reply=False,
#                             reply_markup=usually_kb.subgroup_keyboard(subgroups))
#     else:
#         await bot.send_message(message.chat.id, 'Такой группы не существует!')
#         await state.finish()


# @dp.message_handler(state=states.ScheduleStates.select_subgroup)
# async def state_select_subgroup_schedule(message: types.Message, state: FSMContext):
#     group = (await state.proxy())['group']
#     subgroups = await database.get_subgroups(group)
#     if message.text in [subgroup[0] for subgroup in subgroups]:
#         await add_proxy_data(state, {'subgroup': message.text})
#         days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#         await states.ScheduleStates.select_day.set()
#         await message.reply('Выберите день недели, когда вы хотите добавить расписание', reply=False,
#                             reply_markup=usually_kb.day_keyboard(days))
#     else:
#         await bot.send_message(message.chat.id, 'Такой подгруппы не существует!')
#         await state.finish()


# @dp.message_handler(state=states.ScheduleStates.select_day)
# async def state_select_day_schedule(message: types.Message, state: FSMContext):
#     if message.text in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
#         await add_proxy_data(state, {'day': message.text})
#         await message.reply('Теперь отправьте текст расписания', reply=False,
#                             reply_markup=types.ReplyKeyboardRemove())
#         await states.ScheduleStates.next()
#     else:
#         await bot.send_message(message.chat.id, 'Такого дня недели не существует!')
#         await state.finish()


# @dp.message_handler(state=states.ScheduleStates.schedule_text)
# async def state_schedule_text(message: types.Message, state: FSMContext):
#     schedule_text = message.text
#     await add_proxy_data(state, {'schedule_text': schedule_text})
#     await database.create_schedule(state)
#     await message.reply('Расписание добавлено', reply=False)
#     async with state.proxy() as data:
#         await sending_messages.sending_schedule(data['group'], data['subgroup'], data['day'])
#     await state.finish()


# @dp.message_handler(commands=['next_reply'], is_chat_admin=True)
# async def next_reply_command(message: types.Message):
#     all_qtns = database.get_all_questions()
#     if all_qtns:
#         await states.AnswerTheQuestion.start.set()
#         await bot.send_message(ADMINS_CHAT_ID, f'Вопрос от @{all_qtns[0][2]}:\n'
#                                                f'{all_qtns[0][1]}',
#                                reply_markup=await inline_kb.create_reply_keyboard(all_qtns[0][0]))
#     else:
#         await bot.send_message(ADMINS_CHAT_ID, 'Вопросы закончились')


# @dp.callback_query_handler(Text(startswith='qtn '), state=states.AnswerTheQuestion.start)
# async def callback_question_and_start_state(callback: types.CallbackQuery, state: FSMContext):
#     user_id = callback.data.replace('qtn ', '')
#     await add_proxy_data(state, {'user_id': user_id})
#     await states.AnswerTheQuestion.next()
#     await callback.message.reply('Введите ответ пользователю', reply=False)
#     await callback.answer()


# @dp.message_handler(state=states.AnswerTheQuestion.answer)
# async def answer_the_question(message: types.Message, state: FSMContext):
#     dict_from_proxy = await get_data_from_proxy(state)
#     await bot.send_message(int(dict_from_proxy['user_id']), 'На ваш вопрос ответили: \n'
#                                                             f'{message.text}')
#     await message.reply('Пользователь получил ваш ответ!', reply=False)
#     await database.delete_question(int(dict_from_proxy['user_id']))
#     await state.finish()

# @dp.message_handler(state=states.DeleteDayStates.day_name)
# async def delete_day_state(message: types.Message, state: FSMContext):
#     all_days_names = [name[0] for name in await database.get_all_days()]
#     if message.text in all_days_names:
#         await database.delete_day(message.text)
#         await message.reply('День удален!', reply=False,
#                             reply_markup=types.ReplyKeyboardRemove())
#     else:
#         await bot.send_message(message.chat.id, 'День который вы хотите удалить - не существует!')
#     await state.finish() 

# @dp.message_handler(commands=['create_news'])
# async def create_news(message: types.Message):
#     if message.from_user.id == ADMINS_CHAT_ID:
#         await states.NewsStates.title.set()
#         await message.reply('Отправьте заголовок новости', reply=False)


# @dp.message_handler(state=states.NewsStates.title)
# async def state_title_news(message: types.Message, state: FSMContext):
#     await add_proxy_data(state, {'title': message.text})
#     await message.reply('Теперь введи содержание новости', reply=False)
#     await states.NewsStates.next()


# @dp.message_handler(state=states.NewsStates.content)
# async def state_content_news(message: types.Message, state: FSMContext):
#     await add_proxy_data(state, {'content': message.text})
#     await message.reply('Отправьте фото к новости', reply=False)
#     await states.NewsStates.next()


# @dp.message_handler(state=states.NewsStates.image, content_types=['photo'])
# async def state_image_news(message: types.Message, state: FSMContext):
#     await add_proxy_data(state, {'image': message.photo[0].file_id})
#     await database.add_news(state)
#     await message.reply('Новость успешно создана!', reply=False)
#     await state.finish()


# @dp.message_handler(commands=['delete_news'], is_chat_admin=True)
# async def delete_news(message: types.Message):
#     news = await database.get_news()
#     for i in news:
#         await bot.send_photo(message.chat.id, i[3], f'*НОВОСТЬ*\n\n {i[1]}\n{i[2]}',
#                              parse_mode='Markdown', reply_markup=inline_kb.create_delete_news_keyboard(i[0]))


# @dp.callback_query_handler(Text(startswith='news '))
# async def callback_delete_news(callback: types.CallbackQuery):
#     cb_data = callback.data.replace('news ', '')
#     await database.delete_news(cb_data)
#     await delete_kb.delete_inline_keyboard(callback.message)
#     await callback.answer('Новость удалена!')
#     await bot.send_message(callback.message.chat.id, 'Новость успешно удалена!')
