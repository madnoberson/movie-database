import asyncio
import logging

from .bot import create_bot
from .dispatcher import create_dispatcher
from .config import Config


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    config = Config()

    bot = create_bot(
        tg_config=config.telegram
    )
    dp = create_dispatcher(
        postgres_config=config.postgres,
        yandex_os_config=config.yandex_os
    )

    await dp.start_polling(bot)


asyncio.run(main())

