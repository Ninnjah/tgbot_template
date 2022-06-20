"""User main handlers"""
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils import parts

from tgbot.cb_data import cancel_cb, main_menu_cb
from tgbot.handlers.inline import main_menu
from tgbot.middlewares.locale import _
from tgbot.services.repository import Repo


async def user_start(m: Message, repo: Repo):
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

def register_user(dp: Dispatcher):
    # User start
    dp.register_message_handler(user_start, commands=["start"], state="*")
