"""Admin menu handlers"""
import logging
from typing import Dict

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentTypes, Message
from aiogram.utils import parts

from tgbot.cb_data import admin_add_conf_cb, admin_delete_conf_cb, cancel_cb
from tgbot.handlers.reply import admin_kb
from tgbot.handlers.inline.admin import admin_add_conf_kb, admin_delete_conf_kb
from tgbot.handlers.states.admin.admin_panel import AdminPanelStates
from tgbot.middlewares.locale import _
from tgbot.models.role import UserRole
from tgbot.services.repository import Repo

logger = logging.getLogger(__name__)


async def cancel_handler(callback: CallbackQuery, state: FSMContext):
    # Reset state
    await state.reset_state()
    # Remove message
    await callback.message.delete()
    # Send message about cancel action
    await callback.message.answer(_("Action was canceled"))


async def admin_panel(m: Message):
    await m.reply(
        _(
            "Hello, Admin!"
        ).format(
            user_name=m.from_user.first_name
        ),
        reply_markup=admin_kb.get_kb()
    )


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


# Admins
async def list_admins(m: Message, repo: Repo):
    # Get all admins from database
    user_list = await repo.list_admins()

    # If any admin was found
    if user_list:
        msg_text: str = ""

        # Generate message text
        for num, user in enumerate(user_list, start=1):
            msg_text += _(
                "{num}. <a href='tg://user?id={user_id}'>"
                "<b>{user_id}</b></a> [{date}]\n"
            ).format(
                num=num,
                user_id=user.user_id,
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

    # If no admin was found then send message about it
    else:
        await m.answer(_("No admins was added"))


async def add_admin(m: Message, state: FSMContext):
    # Reseting state
    await state.reset_state()
    # Set add admin state
    await AdminPanelStates.add_admin_state.set()

    # Send message
    await m.answer(
        _(
            "Send user id or forward message "
            "from user who will be an admin"
        )
    )


async def add_admin_handle(m: Message, state: FSMContext, repo: Repo):
    try:
        # If message is forwarded take user id from it
        if getattr(m, "forward_from", None):
            user_id = m.forward_from.id

        # Else get user id from message text
        else:
            user_id: int = int(m.text)

    except ValueError:
        await m.reply(
            _(
                "User id is invalid! Forward to me any message "
                "from this user, or send me his id. You can find it, "
                "for example, from the bot @my_id_bot"
            )
        )
        return

    else:
        # If message from group or channel
        if user_id < 0:
            await m.reply(
                _(
                    "Forwarded message was not sent by user! "
                    "Forward to me any message from this user, "
                    "or send me his id. You can find it, "
                    "for example, from the bot @my_id_bot"
                )
            )
            return

        # If user is not an admin
        elif not await repo.is_admin(user_id):
            await m.answer(
                _(
                    "Are you sure you want to add user {user_id} as an admin?"
                ).format(
                    user_id=user_id
                ),
                reply_markup=admin_add_conf_kb.get_kb(user_id)
            )

        # If user is admin
        else:
            await m.answer(
                _(
                    "User is already an admin"
                )
            )


async def add_admin_conf(
    callback: CallbackQuery,
    callback_data: Dict[str, str],
    state: FSMContext,
    repo: Repo
):
    # Get user id from callback data
    user_id: int = int(callback_data.get("user_id"))

    # Add user to admin table
    await repo.add_admin(user_id=user_id)
    # Finish add admin state
    await state.finish()

    # Log
    logger.info(f"ADMIN {callback.from_user.id} ADD USER {user_id} TO ADMIN")

    # Send success message
    await callback.message.answer(
        _(
            "User {user_id} was added as an admin!"
        ).format(
            user_id=user_id
        )
    )


async def del_admin(m: Message, state: FSMContext):
    # Reseting state
    await state.reset_state()
    # Set del admin state
    await AdminPanelStates.del_admin_state.set()

    # Send message
    await m.answer(
        _(
            "Send user id or forward message "
            "from user who will removed from admins"
        )
    )


async def del_admin_handle(m: Message, state: FSMContext, repo: Repo):
    try:
        # If message is forwarded take user id from it
        if getattr(m, "forward_from", None):
            user_id = m.forward_from.id

        # Else get user id from message text
        else:
            user_id: int = int(m.text)

    except ValueError:
        await m.reply(
            _(
                "User id is invalid! Forward to me any message "
                "from this user, or send me his id. You can find it, "
                "for example, from the bot @my_id_bot"
            )
        )
        return

    else:
        # If message from group or channel
        if user_id < 0:
            await m.reply(
                _(
                    "Forwarded message was not sent by user! "
                    "Forward to me any message from this user, "
                    "or send me his id. You can find it, "
                    "for example, from the bot @my_id_bot"
                )
            )

        # If user is admin
        elif await repo.is_admin(user_id):
            await m.answer(
                _(
                    "Are you sure you want to remove "
                    "user {user_id} from admins?"
                ).format(
                    user_id=user_id
                ),
                reply_markup=admin_delete_conf_kb.get_kb(user_id)
            )

        # If user is not admin
        else:
            await m.answer(
                _(
                    "This user is not an admin"
                )
            )


async def del_admin_conf(
    callback: CallbackQuery,
    callback_data: Dict[str, str],
    state: FSMContext,
    repo: Repo
):
    # Get user id from callback data
    user_id: int = int(callback_data.get("user_id"))

    # Add user to admin table
    await repo.del_admin(user_id=user_id)
    # Finish add admin state
    await state.finish()

    # Log
    logger.info(f"ADMIN {callback.from_user.id} DELETE USER {user_id} FROM ADMINS")

    # Send success message
    await callback.message.answer(
        _(
            "User {user_id} was removed from admins!"
        ).format(
            user_id=user_id
        )
    )


def register_admin(dp: Dispatcher):
    # Admin panel
    dp.register_message_handler(
        admin_panel, commands=["admin"],
        state="*", role=UserRole.ADMIN
    )

    # List users
    dp.register_message_handler(
        list_users, lambda m: m.text == _("List users"),
        state="*", role=UserRole.ADMIN
    )

    # List admins
    dp.register_message_handler(
        list_admins, lambda m: m.text == _("List admins"),
        state="*", role=UserRole.ADMIN
    )

    dp.register_callback_query_handler(
        cancel_handler, cancel_cb.filter(), state="*"
    )

    # Add admin
    dp.register_message_handler(
        add_admin, lambda m: m.text == _("Add admin"),
        state="*", role=UserRole.ADMIN
    )
    dp.register_message_handler(
        add_admin_handle, content_types=ContentTypes.ANY,
        state=AdminPanelStates.add_admin_state, role=UserRole.ADMIN
    )
    dp.register_callback_query_handler(
        add_admin_conf, admin_add_conf_cb.filter(),
        state=AdminPanelStates.add_admin_state
    )

    # Delete admin
    dp.register_message_handler(
        del_admin, lambda m: m.text == _("Delete admin"),
        state="*", role=UserRole.ADMIN
    )
    dp.register_message_handler(
        del_admin_handle, content_types=ContentTypes.ANY,
        state=AdminPanelStates.del_admin_state, role=UserRole.ADMIN
    )
    dp.register_callback_query_handler(
        del_admin_conf, admin_delete_conf_cb.filter(),
        state=AdminPanelStates.del_admin_state
    )
    # # or you can pass multiple roles:
    # dp.register_message_handler(
    #     admin_panel, commands=["admin"],
    #     state="*", role=[UserRole.ADMIN]
    # )
    # # or use another filter:
    # dp.register_message_handler(
    #     admin_panel, commands=["admin"],
    #     state="*", is_admin=True
    # )
