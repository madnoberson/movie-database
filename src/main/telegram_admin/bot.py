from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode

from .config import TelegramConfig


def create_bot(tg_config: TelegramConfig) -> Bot:
    bot = Bot(
        token=tg_config.telegram_bot_token,
        parse_mode=ParseMode.HTML
    )

    return bot
