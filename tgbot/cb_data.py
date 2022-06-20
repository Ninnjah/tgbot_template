"""Create callback data for inline keyboards"""
from aiogram.utils.callback_data import CallbackData

main_menu_cb = CallbackData("main_menu", "menu")

projects_callback = CallbackData("projects", "view")

cancel_cb = CallbackData("cancel")
admin_add_conf_cb = CallbackData("admin_add_conf", "user_id")
admin_delete_conf_cb = CallbackData("admin_delete_conf", "user_id")
