from faststream import FastStream

from . import config


async def setup_dependencies(
    app: FastStream, database_config: config.DatabaseConfig
) -> None:
    ...