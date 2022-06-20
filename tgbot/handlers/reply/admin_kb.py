"""Admin panel main reply keyboard"""
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

from tgbot.middlewares.locale import _


def get_kb():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    keyboard.add(
        KeyboardButton(_("List users"))
    )
    keyboard.add(
        KeyboardButton(_("List admins"))
    )
    keyboard.add(
        KeyboardButton(_("Add admin")),
        KeyboardButton(_("Delete admin")),
    )

    return keyboard
