import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from dotenv import load_dotenv
if __name__ == "__main__":
    load_dotenv(".env")

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.pool import QueuePool

from tgbot.config import load_config
from tgbot.database.tables import metadata
from tgbot.filters.role import RoleFilter, AdminFilter

from tgbot.handlers.admin import (
    admin_panel, admin_admins, admin_users, admin_localisation
)
from tgbot.handlers.user import user_start

from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.role import RoleMiddleware
from tgbot.middlewares.locale import i18n
from tgbot.middlewares.mediagroup import AlbumMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware

logger = logging.getLogger(__name__)


async def create_pool(database_url: str, echo: bool) -> AsyncEngine:
    """Create connection pool to database

    :param database_url: Database url
    :type database_url: str
    :param echo: Echo parameter
    :type echo: bool
    :return: Async connection engine
    :rtype: AsyncEngine
    """
    engine = create_async_engine(
        database_url, pool_size=5, max_overflow=0,
        poolclass=QueuePool, echo=echo
    )

    async with engine.begin() as conn:
        # Create tables in database
        await conn.run_sync(metadata.create_all)

    # Return connection engine
    return engine


async def main():
    """Bot initializator"""
    # Setup logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    # Load config
    config = load_config()

    # Setup FSM storage
    if config.tg_bot.use_redis:
        storage = RedisStorage2()
    else:
        storage = MemoryStorage()

    # Create database connection pool
    pool = await create_pool(
        database_url=config.db.database_url,
        echo=False,
    )

    # Create bot instance
    bot = Bot(token=config.tg_bot.token, parse_mode="html")
    # Create Dispatcher instance
    dp = Dispatcher(bot, storage=storage)

    # Setup database middleware
    dp.middleware.setup(DbMiddleware(pool))
    # Setup role middleware
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_list))
    # Setup mediagroup middleware
    dp.middleware.setup(AlbumMiddleware())
    # Setup throttling middleware
    dp.middleware.setup(ThrottlingMiddleware())
    # Setup localisation middleware
    dp.middleware.setup(i18n)
    # Create role filters
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    # Register admin handlers
    admin_panel.register(dp)
    admin_admins.register(dp)
    admin_users.register(dp)
    admin_localisation.register(dp)

    # Register user handlers
    user_start.register(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
