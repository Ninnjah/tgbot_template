"""Inline keyboard for add admin confirmation"""
from aiogram.types.inline_keyboard import InlineKeyboardButton, \
    InlineKeyboardMarkup

from tgbot.cb_data import admin_add_conf_cb, cancel_cb
from tgbot.middlewares.locale import _


def get_kb(user_id: int) -> InlineKeyboardMarkup:
    # Create keyboard
    keyboard = InlineKeyboardMarkup(row_width=2)

    # Add button with text and callback data
    keyboard.add(
        InlineKeyboardButton(
            text=_("Yes"),
            callback_data=admin_add_conf_cb.new(
                user_id=user_id
            )
        ),
        InlineKeyboardButton(
            text=_("No"),
            callback_data=cancel_cb.new()
        ),
    )

    # Return keyboard
    return keyboard
