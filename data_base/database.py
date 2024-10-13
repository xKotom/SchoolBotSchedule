import sqlite3
from datetime import datetime
from sqlite3 import IntegrityError
from c_bot import bot


conn = sqlite3.connect('sched.db')
cursor = conn.cursor()

# Группа: 11, Буква: А, День: Понедельник

def sql_start():
    if conn: 
        print(f"База данных подключена!{sqlite3.version}")
    cursor.execute('CREATE TABLE IF NOT EXISTS users (tg_id INTEGER, name_group TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS groups (name TEXT PRIMARY KEY, schedule TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS subgroups (name TEXT, group_name TEXT, schedule TEXT, day_name TEXT, PRIMARY KEY (name, group_name), FOREIGN KEY (group_name) REFERENCES groups (name))')
    cursor.execute('CREATE TABLE IF NOT EXISTS days (day TEXT, subgroup_name TEXT, subgroup_group_name TEXT, PRIMARY KEY (day, subgroup_name, subgroup_group_name), FOREIGN KEY (subgroup_name, subgroup_group_name) REFERENCES subgroups (name, group_name))')
    cursor.execute('CREATE TABLE IF NOT EXISTS schedules (id INTEGER PRIMARY KEY, subgroup_name TEXT, group_name TEXT, day_name TEXT, schedule_text TEXT, FOREIGN KEY (subgroup_name, group_name) REFERENCES subgroups (name, group_name))')
    conn.commit()
    conn.commit()
    print("Таблица создана!")
    return conn, cursor 


# proxy
async def get_data_from_proxy(state):
    async with state.proxy() as data:
        return data
    
# group - групп классов 

async def get_all_groups():
    return [_ for _ in cursor.execute('SELECT * FROM groups')]


async def delete_group(name):
    cursor.execute('DELETE FROM groups WHERE name = ?', (name,))
    conn.commit()


async def add_group(name, msg):
    try:
        cursor.execute('INSERT INTO groups VALUES (?, ?)', (name, None))
        conn.commit()
    except IntegrityError:
        await bot.send_message(msg.chat.id, 'Данная группа уже создана!')

# async def get_group(name):
#     return [i for i in cursor.execute('SELECT * FROM groups WHERE name = ?', (name,))]
async def get_group(name):
    cursor.execute('SELECT * FROM groups WHERE name = ?', (name,))
    return await cursor.fetchall()


# subgroup
async def create_subgroup(group_name, subgroup_name, msg, schedule='', day_name=''):
    try:
        # Создание подгруппы (класса)
        cursor.execute('''
            INSERT INTO subgroups (name, group_name, schedule, day_name)
            VALUES (?, ?, ?, ?)
        ''', (subgroup_name, group_name, schedule, day_name))
        conn.commit()

        # Автоматизация дней недели
        default_days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        for day in default_days:
            cursor.execute('''
                INSERT OR IGNORE INTO days (day, subgroup_name, subgroup_group_name)
                VALUES (?, ?, ?)
            ''', (day, subgroup_name, group_name))
        conn.commit()
    except IntegrityError:
        await bot.send_message(msg.chat.id, 'Данная подгруппа уже создана!')

async def get_subgroups(group_name):
    return [i for i in cursor.execute('SELECT * FROM subgroups WHERE group_name = ?', (group_name,))]

async def delete_subgroup(group_name, subgroup_name):
    cursor.execute('DELETE FROM subgroups WHERE group_name = ? AND name = ?', (group_name, subgroup_name))
    conn.commit()


# schedule  - расписание 
async def create_schedule(state, day_name, subgroup_name, group_name, schedule_text):
    cursor.execute('INSERT INTO schedules (subgroup_name, group_name, day_name, schedule_text) VALUES (?, ?, ?, ?)',
                         (subgroup_name, group_name, day_name, schedule_text))
    conn.commit()

async def get_schedule(group_name, subgroup_name, day_name):
    print(f"Входные данные в бд: subgroup_name={subgroup_name}, group_name={group_name}, day_name={day_name}")
    cursor.execute('SELECT schedule_text FROM schedules WHERE subgroup_name = ? AND group_name = ? AND day_name = ?',
                   (subgroup_name, group_name, day_name))
    result = cursor.fetchone()
    print(f"Result: {result}")
    if result:
        return result[0]
    else:
        return None

async def delete_schedule(group_name, subgroup_name, day_name):
    print(f"Входные данные в бд: group_name={group_name}, subgroup_name={subgroup_name}, day_name={day_name}")
    cursor.execute('DELETE FROM schedules WHERE group_name = ? AND subgroup_name = ? AND day_name = ?',
                   (group_name, subgroup_name, day_name))
    result = cursor.fetchone()
    print(f"Result: {result}")
    conn.commit()


# user 
async def add_user(user_id):
    cursor.execute('INSERT INTO users VALUES (?, ?)', (user_id, 'no_group'))
    conn.commit()

async def get_all_users():
    return [u for u in cursor.execute('SELECT * FROM users')]

async def change_user_group(user_id, group_name):
    cursor.execute('UPDATE users SET name_group = ? WHERE tg_id = ?', (group_name, user_id))
    conn.commit()        

async def get_only_such_users(name):
    return [i for i in cursor.execute('SELECT * FROM users WHERE name_group = ?', (name,))]

async def change_user_subgroup(user_id, subgroup_name, group_name):
    cursor.execute('UPDATE users SET subgroup_name = ?, subgroup_group_name = ? WHERE tg_id = ?', (subgroup_name, group_name, user_id))
    conn.commit()


# days
async def get_days(subgroup_name, group_name):
    return [i for i in cursor.execute('SELECT * FROM days WHERE subgroup_name = ? AND subgroup_group_name = ?', (subgroup_name, group_name))]


async def add_day(subgroup_name, group_name, day, msg):
    try:
        cursor.execute('INSERT INTO days VALUES (?, ?, ?)', (day, subgroup_name, group_name))
        conn.commit()
    except IntegrityError:
        bot.send_message(msg.chat.id, 'День недели уже добавлен!')

