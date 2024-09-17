
# async def add_day(subgroup_name, group_name, day, msg):
#     try:
#         cursor.execute('INSERT INTO days VALUES (?, ?, ?)', (day, subgroup_name, group_name))
#         conn.commit()
#     except IntegrityError:
#         bot.send_message(msg.chat.id, 'День недели уже добавлен!')


# async def create_schedule(state, day_name):
#     data = await get_data_from_proxy(state)
#     subgroup_name = await get_only_such_users(state.user_id)[0][1]
#     group_name = await get_only_such_users(state.user_id)[0][1]
#     schedule_text = '\n'.join([f'{lesson} - {time}' for lesson, time in data['lessons']])
#     cursor.execute('UPDATE subgroups SET schedule = ?, day_name = ? WHERE name = ? AND group_name = ?',
#                    (schedule_text, day_name, subgroup_name, group_name))
#     conn.commit()