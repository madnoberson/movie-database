import asyncio

from .server import create_server
from .app import create_app


async def main() -> None:
    app = create_app()
    server = create_server(app)

    await server.serve()


asyncio.run(main())