"""States for admin panel"""
from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminPanelStates(StatesGroup):
    # State for input admin's user id
    # for add them to DB
    add_admin_state = State()
    # State for input admin's user id
    # for delete them from DB
    del_admin_state = State()
