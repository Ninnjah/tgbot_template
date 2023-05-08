"""User main handlers"""
from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.middlewares.locale import _
from tgbot.services.repository import Repo


async def start(m: Message, repo: Repo):
    # Add user to database
    await repo.add_user(
        user_id=m.from_user.id,
        firstname=m.from_user.first_name,
        fullname=m.from_user.full_name,
        lastname=m.from_user.last_name,
        username=m.from_user.username
    )

    # Send message to user with inline example keyboard
    await m.reply(
        _("Hello, User!"),
    )


def register(dp: Dispatcher):
    # User start
    dp.register_message_handler(start, commands=["start"], state="*")
