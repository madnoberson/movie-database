import asyncio

from .config import load_config
from .app import create_app
from .server import create_server


async def main() -> None:
    config = load_config()

    app = await create_app(
        fastapi_config=config.fastapi, database_config=config.database,
        event_bus_config=config.event_bus,
        session_gateway_config=config.session_gateway
    )
    server = create_server(app, config.uvicorn)

    await server.serve()


asyncio.run(main())