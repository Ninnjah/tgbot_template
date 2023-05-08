"""Admin menu handlers"""
import logging
from typing import Dict

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentTypes, Message
from aiogram.utils import parts

from tgbot.cb_data import yesno_cb
from tgbot.handlers.inline import yesno_kb
from tgbot.handlers.states.admin.admin_panel import ManageAdminStates
from tgbot.middlewares.locale import _
from tgbot.models.role import UserRole
from tgbot.services.repository import Repo

logger = logging.getLogger(__name__)
GOAL = "admin"


# List admins
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


# Add admins
async def add_admin(m: Message, state: FSMContext):
    # Reseting state
    await state.reset_state()
    # Set add admin state
    await state.set_state(ManageAdminStates.add_admin.state)

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
                reply_markup=yesno_kb.get(f"add_{GOAL}", user_id)
            )

        # If user is admin
        else:
            await m.answer(_("User is already an admin"))


async def add_admin_conf(
    callback: CallbackQuery,
    callback_data: Dict[str, str],
    state: FSMContext,
    repo: Repo
):
    # Get user id from callback data
    user_id: int = int(callback_data.get("data"))

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


async def add_admin_cancel(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(_("Action was canceled"))


# Delete admins
async def del_admin(m: Message, state: FSMContext):
    # Reseting state
    await state.reset_state()
    # Set del admin state
    await state.set_state(ManageAdminStates.del_admin.state())

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
                reply_markup=yesno_kb.get(f"del_{GOAL}", user_id)
            )

        # If user is not admin
        else:
            await m.answer(_("This user is not an admin"))


async def del_admin_conf(
    callback: CallbackQuery,
    callback_data: Dict[str, str],
    state: FSMContext,
    repo: Repo
):
    # Get user id from callback data
    user_id: int = int(callback_data.get("data"))

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


async def del_admin_cancel(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(_("Action was canceled"))


def register(dp: Dispatcher):
    # List admins
    dp.register_message_handler(
        list_admins, lambda m: m.text == _("List admins"),
        state="*", role=UserRole.ADMIN
    )

    # Add admin
    dp.register_message_handler(
        add_admin, lambda m: m.text == _("Add admin"),
        state="*", role=UserRole.ADMIN
    )
    dp.register_message_handler(
        add_admin_handle, content_types=ContentTypes.ANY,
        state=ManageAdminStates.add_admin, role=UserRole.ADMIN
    )
    dp.register_callback_query_handler(
        add_admin_conf, yesno_cb.filter(action=f"add_{GOAL}", value="1"),
        state=ManageAdminStates.add_admin
    )
    dp.register_callback_query_handler(
        add_admin_cancel, yesno_cb.filter(action=f"add_{GOAL}", value="0"),
        state=ManageAdminStates.add_admin
    )

    # Delete admin
    dp.register_message_handler(
        del_admin, lambda m: m.text == _("Delete admin"),
        state="*", role=UserRole.ADMIN
    )
    dp.register_message_handler(
        del_admin_handle, content_types=ContentTypes.ANY,
        state=ManageAdminStates.del_admin, role=UserRole.ADMIN
    )
    dp.register_callback_query_handler(
        del_admin_conf, yesno_cb.filter(action=f"del_{GOAL}", value="1"),
        state=ManageAdminStates.del_admin
    )
    dp.register_callback_query_handler(
        del_admin_cancel, yesno_cb.filter(action=f"del_{GOAL}", value="0"),
        state=ManageAdminStates.del_admin
    )
