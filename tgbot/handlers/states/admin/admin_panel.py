"""States for admin panel"""
from aiogram.dispatcher.filters.state import State, StatesGroup


class ManageAdminStates(StatesGroup):
    add_admin = State()
    del_admin = State()
