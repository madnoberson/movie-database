from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode

from .config import TelegramConfig


def create_bot(telegram_config: TelegramConfig) -> Bot:
    return Bot(token=telegram_config.token, parse_mode=ParseMode.HTML)