from faststream import FastStream
from faststream.rabbit import RabbitBroker

from app.main import config
from .dependencies import setup_dependencies


async def create_app(
    faststream_config: config.FastStreamConfig,
    database_config: config.DatabaseConfig
) -> FastStream:
    broker = RabbitBroker(
        host=faststream_config.rq_host, port=faststream_config.rq_port,
        login=faststream_config.rq_login, password=faststream_config.rq_password
    )
    
    app = FastStream(
        broker=broker, title=faststream_config.title,
        version=faststream_config.version, description=faststream_config.description
    )
    await setup_dependencies(app=app, database_config=database_config)

    return app