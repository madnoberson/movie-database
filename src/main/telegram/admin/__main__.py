import asyncio
import logging

from .config import Config
from .bot import create_bot
from .dispatcher import create_dispatcher


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    config = Config()

    bot = create_bot(config.telegram)
    dispatcher = await create_dispatcher(config.postgres)

    await dispatcher.start_polling(bot)


asyncio.run(main())