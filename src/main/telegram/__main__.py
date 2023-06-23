import asyncio
import logging

from .bot import create_bot
from .dispatcher import create_dipatcher
from .config import Config


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    config = Config()

    bot = create_bot(config)
    dp = create_dipatcher()

    await dp.start_polling(bot)


asyncio.run(main())