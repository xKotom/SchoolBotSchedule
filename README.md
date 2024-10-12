# ENG
# Telegram Bot for Schedules

This project is a Telegram bot that allows users to manage and retrieve information about schedules for various groups and subgroups. The bot uses SQLite for data storage and provides various functions for creating and managing schedules.

## Features

- **User Management**: Adding and managing users and their groups.
- **Group Management**: Creating, deleting, and retrieving information about groups.
- **Subgroup Management**: Creating and managing subgroups within each group, including automatic addition of weekdays.
- **Schedule Management**: Creating, retrieving, and deleting schedules for specific subgroups on designated days.
- **Day Management**: Adding and managing weekdays for subgroups.

## Requirements

- Python 3.11.5
- `aiogram 2.25.2` library
- `sqlite3` database

## Installation

1. Required packages
   ```bash
   pip install aiogram==2.25.2
   pip install db-sqlite3
   ```

## Usage

1. **Bot Setup**:
   ```python
   bot = Bot(token="TOKEN_BOT")
   ADMINS_CHAT_ID = ID_ADMIN
   ```

2. **Run the bot**:
   The bot is run through main_bot.py
   ```bash
   python main_bot.py
   ```

3. **Interacting with the bot**:
   The bot can process various commands related to managing groups, subgroups, and schedules.

### Admin Command Overview
- **/start**: Start interacting with the bot.
- **/add_group <group_name>**: Create a new group.
- **/delete_group <group_name>**: Delete an existing group.
- **/create_subgroup <group_name> <subgroup_name>**: Create a new subgroup.
- **/add_schedule <subgroup_name> <group_name> <day_name> <schedule_text>**: Add a schedule for the subgroup on a specific day.
- **/get_schedule <subgroup_name> <group_name> <day_name>**: Retrieve the schedule for a specific subgroup and day.
- **/help**: Show available commands.

## Database Schema

The SQLite database consists of the following tables:

- **users**: Stores user data.
- **groups**: Contains information about various groups.
- **subgroups**: Includes subgroups related to groups.
- **days**: Contains weekdays associated with subgroups.
- **schedules**: Stores the actual schedule for each subgroup on a specific day.

### User Command Overview
- **/start**: Start interacting with the bot and register in the system.
- **/view_schedule**: Begin the process of viewing the schedule.
  - **Group Selection**: Choose a group (class) to view the schedule.
  - **Subgroup Selection**: Choose a subgroup (letter of the class) to retrieve the schedule.
  - **Day Selection**: Choose a weekday to view the schedule.
- **/help**: Show available commands and contact information for assistance.
- **Exit**: Finish the schedule viewing process and return to the main menu.
---
# RU
# Телеграмм Бот для Расписаний

Этот проект представляет собой Телеграмм бота, который позволяет пользователям управлять и получать информацию о расписаниях для различных групп и подгрупп. Бот использует SQLite для хранения данных и предоставляет различные функции для создания и управления расписаниями.

## Возможности

- **Управление пользователями**: Добавление и управление пользователями и их группами.
- **Управление группами**: Создание, удаление и получение информации о группах.
- **Управление подгруппами**: Создание и управление подгруппами в каждой группе, включая автоматическое добавление дней недели.
- **Управление расписаниями**: Создание, получение и удаление расписаний для конкретных подгрупп в определенные дни.
- **Управление днями**: Добавление и управление днями недели для подгрупп.

## Требования

- Python 3.11.5
- Библиотека `aiogram 2.25.2 `
- СУБД `sqlite3` 

## Установка

1. Необходимые пакеты
   ```bash
   pip install aiogram==2.25.2
   pip install db-sqlite3
   ```

## Использование

1. **Настройка бота**:
   ```python
   bot = Bot(token="TOKEN_BOT")
   ADMINS_CHAT_ID = ID_ADMIN
   ```

2. **Запустите бота**:
   Запуск бота происходит через main_bot.py
   ```bash
   python main_bot.py
   ```

3. **Взаимодействие с ботом**:
   Бот может обрабатывать различные команды, связанные с управлением группами, подгруппами и расписаниями.

### Обзор команд для администратора
- **/start**: Начать взаимодействие с ботом.
- **/add_group <имя_группы>**: Создать новую группу.
- **/delete_group <имя_группы>**: Удалить существующую группу.
- **/create_subgroup <имя_группы> <имя_подгруппы>**: Создать новую подгруппу.
- **/add_schedule <имя_подгруппы> <имя_группы> <имя_дня> <текст_расписания>**: Добавить расписание для подгруппы на конкретный день.
- **/get_schedule <имя_подгруппы> <имя_группы> <имя_дня>**: Получить расписание для конкретной подгруппы и дня.
- **/help**: Показать доступные команды.

## Схема базы данных

База данных SQLite состоит из следующих таблиц:

- **users**: Хранит данные пользователей.
- **groups**: Содержит информацию о различных группах.
- **subgroups**: Включает подгруппы, относящиеся к группам.
- **days**: Содержит дни недели, связанные с подгруппами.
- **schedules**: Хранит фактическое расписание для каждой подгруппы на конкретный день.

### Команды для пользователя 

Обзор команд
- **/start**: Начать взаимодействие с ботом и зарегистрироваться в системе.
- **/view_schedule**: Начать процесс просмотра расписания.
  - **Выбор группы**: Выберите группу (класс) для просмотра расписания.
  - **Выбор подгруппы**: Выберите подгруппу (букву класса) для получения расписания.
  - **Выбор дня**: Выберите день недели для просмотра расписания.
- **/help**: Показать доступные команды и контактную информацию для получения помощи.
- **Выйти**: Завершить процесс просмотра расписания и выйти в главное меню.

--- 
