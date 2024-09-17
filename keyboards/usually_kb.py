from aiogram import types
from data_base import database
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def group_keyboard(group_list):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for group in group_list:
        but = types.KeyboardButton(group[0])
        kb.add(but)
    return kb

def subgroup_keyboard(subgroup_list):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subgroup in subgroup_list:
        but = types.KeyboardButton(subgroup[0])
        kb.add(but)
    return kb

async def day_keyboard(subgroup_name, group_name, db):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    days = await database.get_days(subgroup_name, group_name)
    for day in days:
        but = types.KeyboardButton(day[0])
        kb.add(but)
    return kb



def view_sche_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_view_schedule = types.KeyboardButton('Просмотреть расписание')
    kb.add(btn_view_schedule)
    return kb

def cmd_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_create_group = types.KeyboardButton('Создать группу ✅')
    btn_delete_group = types.KeyboardButton('Удалить группу ❌')
    btn_create_subgroup = types.KeyboardButton('Создать подгруппу ✅')
    btn_delete_subgroup = types.KeyboardButton('Удалить подгруппу ❌')
    btn_create_schedule = types.KeyboardButton('Создать расписание ✅')
    btn_delete_schedule = types.KeyboardButton('Удалить расписание ❌')
    btn_view_schedule = types.KeyboardButton('Просмотр расписания 👀')
    
    kb.add(btn_create_group)
    kb.add(btn_create_subgroup)
    kb.add(btn_create_schedule)
    kb.add(btn_delete_group)
    kb.add(btn_delete_subgroup)
    kb.add(btn_delete_schedule)
    kb.add(btn_view_schedule)
    
    return kb