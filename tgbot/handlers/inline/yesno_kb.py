"""Inline keyboard for add admin confirmation"""
from typing import Any

from aiogram.types.inline_keyboard import InlineKeyboardButton, \
    InlineKeyboardMarkup

from tgbot.cb_data import yesno_cb
from tgbot.middlewares.locale import _


def get(action: str, data: Any = "") -> InlineKeyboardMarkup:
    # Create keyboard
    keyboard = InlineKeyboardMarkup(row_width=2)

    # Add button with text and callback data
    keyboard.add(
        InlineKeyboardButton(
            text=_("Yes"),
            callback_data=yesno_cb.new(
                action=action,
                data=data,
                value=1
            )
        ),
        InlineKeyboardButton(
            text=_("No"),
            callback_data=yesno_cb.new(
                action=action,
                data=data,
                value=0
            )
        ),
    )

    # Return keyboard
    return keyboard
