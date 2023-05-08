"""Admin menu handlers"""
import logging
from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.handlers.reply import admin_kb
from tgbot.middlewares.locale import _
from tgbot.models.role import UserRole

logger = logging.getLogger(__name__)


async def admin_panel(m: Message):
    await m.reply(
        _(
            "Hello, Admin!"
        ).format(
            user_name=m.from_user.first_name
        ),
        reply_markup=admin_kb.get()
    )


def register(dp: Dispatcher):
    # Admin panel
    dp.register_message_handler(
        admin_panel, commands=["admin"],
        state="*", role=UserRole.ADMIN
    )