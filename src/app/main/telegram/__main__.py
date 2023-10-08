import os
import asyncio
import logging

from app.main.common.utils.config_loader import load_config
from .config import Config
from .bot import create_bot
from .dispatcher import create_dispatcher


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    config = load_config(Config, os.getenv("CONFIG_PATH"))
    bot = create_bot(config.telegram)
    dispatcher = await create_dispatcher(config.postgres)

    await dispatcher.start_polling(bot)


asyncio.run(main())