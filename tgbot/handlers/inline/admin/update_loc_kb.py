"""Inline keyboard for add admin confirmation"""
from aiogram.types.inline_keyboard import InlineKeyboardButton, \
    InlineKeyboardMarkup

from tgbot.cb_data import update_loc_cb

LOCALISATIONS = {
    "ru": "🇷🇺",
    "en": "🇬🇧"
}


def get() -> InlineKeyboardMarkup:
    # Create keyboard
    keyboard = InlineKeyboardMarkup()

    # Add button with text and callback data
    for lang, flag in LOCALISATIONS.items():
        keyboard.insert(
            InlineKeyboardButton(
                text=flag,
                callback_data=update_loc_cb.new(
                    lang=lang
                )
            ),
        )

    # Return keyboard
    return keyboard
