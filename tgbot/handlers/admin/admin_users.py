"""Admin menu handlers"""
import logging

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils import parts

from tgbot.middlewares.locale import _
from tgbot.models.role import UserRole
from tgbot.services.repository import Repo

logger = logging.getLogger(__name__)


# Users
async def list_users(m: Message, repo: Repo):
    # Get all users from database
    user_list = await repo.list_users()

    # If any user was found
    if user_list:
        msg_text: str = ""

        # Generate message text
        for num, user in enumerate(user_list, start=1):
            username = f"@{user.username}" if user.username is not None else ""
            msg_text += _(
                "{num}. {user_id} "
                "<a href='tg://user?id={user_id}'><b>{fullname}</b></a> "
                "{username}[{date}]\n"
            ).format(
                num=num,
                user_id=user.user_id,
                fullname=user.fullname,
                username=username,
                date=user.created_on
            )

        # If message long than maximum possible message
        # then split message text on parts
        if len(msg_text) > parts.MAX_MESSAGE_LENGTH:
            for message in parts.safe_split_text(
                msg_text, split_separator="\n"
            ):
                await m.answer(message)

        # Else simply send this message text
        else:
            await m.answer(msg_text)

    # If no users was found then send message about it
    else:
        await m.answer(_("No users was found"))


def register(dp: Dispatcher):
    # List users
    dp.register_message_handler(
        list_users, lambda m: m.text == _("List users"),
        state="*", role=UserRole.ADMIN
    )
