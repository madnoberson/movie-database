from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode

from .config import TelegramConfig


def create_bot(config: TelegramConfig) -> Bot:
    bot = Bot(
        token=config.token,
        parse_mode=ParseMode.HTML
    )
    return bot
