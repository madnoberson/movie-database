import asyncio

from .config import load_config
from .app import create_app


async def main() -> None:
    config = load_config()

    app = create_app(config.faststream)

    await app.run()


asyncio.run(main())