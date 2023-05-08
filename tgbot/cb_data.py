"""Create callback data for inline keyboards"""
from aiogram.utils.callback_data import CallbackData

yesno_cb = CallbackData("yn", "action", "value", "data")
main_menu_cb = CallbackData("main_menu", "menu")
cancel_cb = CallbackData("cancel")

update_loc_cb = CallbackData("ul", "lang")
