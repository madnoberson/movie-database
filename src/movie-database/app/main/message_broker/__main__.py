import asyncio

from app.main.config import load_message_broker_config
from .app import create_app


async def main() -> None:
    config = load_message_broker_config()

    app = await create_app(
        faststream_config=config.faststream,
        database_config=config.database
    )

    await app.run()


asyncio.run(main())