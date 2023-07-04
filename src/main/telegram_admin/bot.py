from aiogram import Bot

from .config import TelegramConfig


def create_bot(tg_config: TelegramConfig) -> Bot:
    bot = Bot(tg_config.telegram_bot_token)
    return bot
