"""Update localisation handlers"""
import logging
from subprocess import run
from pathlib import Path
from typing import Dict

from aiogram import Dispatcher
from aiogram.types import (
    Message, InputFile, ContentType, CallbackQuery
)

from tgbot.cb_data import update_loc_cb
from tgbot.middlewares.locale import _
from tgbot.models.role import UserRole
from tgbot.handlers.inline.admin import update_loc_kb
from tgbot.middlewares.locale import I18N_DOMAIN, i18n

logger = logging.getLogger(__name__)
LOCALES_PATH = Path("locales")
POT_PATH = LOCALES_PATH / Path(f"{I18N_DOMAIN}.pot")


async def get_pot_handler(m: Message):
    await m.answer_document(
        InputFile(POT_PATH), 
        caption=_("Create localisation from this template and upload it")
    )


async def update_loc_query(m: Message):
    await m.reply(
        _("Which language you want to update?"),
        reply_markup=update_loc_kb.get()
    )

async def update_loc_handler(callback: CallbackQuery, callback_data: Dict[str, str]):
    locale_path = LOCALES_PATH / Path(
            callback_data["lang"], "LC_MESSAGES", f"{I18N_DOMAIN}.po"
        )
    locale_path.parents[0].mkdir(exist_ok=True, parents=True)
    
    with locale_path.open("wb") as f:
        await callback.bot.download_file_by_id(
            file_id=callback.message.reply_to_message.document.file_id,
            destination=f
        )
    
    run(f"pybabel compile -d locales -D {I18N_DOMAIN}")
    i18n.reload()

    await callback.message.answer(_("Locale updated!"))



def register(dp: Dispatcher):
    dp.register_message_handler(
        get_pot_handler, lambda m: m.text == _("Get template"),
        state="*", role=UserRole.ADMIN
    )
    dp.register_message_handler(
        update_loc_query, lambda m: m.document.file_name.endswith(".po"),
        content_types=ContentType.DOCUMENT, role=UserRole.ADMIN
    )
    dp.register_callback_query_handler(
        update_loc_handler, update_loc_cb.filter(),
        role=UserRole.ADMIN
    )
