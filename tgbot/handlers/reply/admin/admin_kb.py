"""Admin panel main reply keyboard"""
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

from tgbot.middlewares.locale import _


def get():
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
    keyboard.add(
        KeyboardButton(_("Get template"))
    )

    return keyboard
