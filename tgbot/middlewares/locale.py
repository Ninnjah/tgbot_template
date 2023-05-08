"""This middleware need for bot localisation

Step 1: extract texts
    run `pybabel extract --input_dir=./tgbot -o locales/teamder-bot.pot` to
    extract all locale strings

Step 2: create *.po files
    `pybabel init -i locales/mybot.pot -d locales -D teamder-bot -l en`
    `pybabel init -i locales/mybot.pot -d locales -D teamder-bot -l ru`

Step 3: translate texts located in locales/{language}/LC_MESSAGES/mybot.po
    To open .po file you can use basic text editor or any PO
    editor, e.g. https://poedit.net/

Step 4: compile translations
    run `pybabel compile -d locales -D teamder-bot` to compile all
    localisation files
"""
from pathlib import Path
from subprocess import run

from aiogram.contrib.middlewares.i18n import I18nMiddleware

from tgbot.config import load_config


config = load_config()

# Name for localisation files
I18N_DOMAIN = config.tg_bot.domain

# Bot directory
BASE_DIR = Path(__name__).parent
# Locales directory
LOCALES_DIR = BASE_DIR / "locales"

run(f"pybabel compile -d locales -D {I18N_DOMAIN}")
# Localisation middleware
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)

# Alias for gettext method
_ = i18n.gettext
