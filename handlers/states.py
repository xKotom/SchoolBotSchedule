from aiogram.dispatcher.filters.state import State, StatesGroup



class NewsStates(StatesGroup):
    title = State()
    content = State()
    image = State()

# Group - класс
class CreateGroupStates(StatesGroup):
    group_name = State()

class SelectGroupStates(StatesGroup):
    group_name = State()
    subgroup_name = State()
    day_name = State()

class DeleteGroupStates(StatesGroup):
    group_name = State()

class StartStates(StatesGroup):
    group_name = State()
    subgroup_name = State()
    day_name = State()

# Schedule - расписание
class ScheduleStates(StatesGroup):
    select_subgroup = State()
    select_day = State()
    schedule_text = State()
    select_group = State()

class CreateScheduleStates(StatesGroup):
    group_name = State()
    subgroup_name = State()
    day_name = State()
    schedule_text = State()

class ViewScheduleStates(StatesGroup):
    group_name = State()
    subgroup_name = State()
    day_name = State()
    schedule_text = State()

class DeleteScheduleStates(StatesGroup):
    group_name = State()
    subgroup_name = State()
    day_name = State()
    schedule_text = State()


# Subgroup - подгруппа
class CreateSubgroupStates(StatesGroup):
    group_name = State()
    subgroup_name = State()


class DeleteSubgroupStates(StatesGroup):
    group_name = State()
    subgroup_name = State()


class UpdateSubgroupStates(StatesGroup):
    subgroup_name = State()
    new_subgroup_name = State()


# day - дни НЕ РАБОТАЮТ 
class CreateDayStates(StatesGroup):
    group_name = State()
    subgroup_name = State()
    days_name = State()
    


class DeleteDayStates(StatesGroup):
    group_name = State()
    subgroup_name = State()
    days_name = State()
    