import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker


async def main() -> None:
    app = FastStream()
    ...


asyncio.run(main())