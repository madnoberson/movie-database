import asyncio

from .server import create_server
from .app import create_app
from .config import Config


async def main() -> None:
    config = Config()

    app = create_app(config)
    server = create_server(app, config.uvicorn)

    await server.serve()


asyncio.run(main())