import asyncio

from app.main.config import load_web_api_config
from .app import create_app
from .server import create_server


async def main() -> None:
    config = load_web_api_config()

    app = await create_app(
        fastapi_config=config.fastapi,
        database_config=config.database,
        event_bus_config=config.event_bus,
        identity_provider_config=config.identity_provider
    )
    server = create_server(
        app=app, uvicorn_config=config.uvicorn
    )

    await server.serve()


asyncio.run(main())