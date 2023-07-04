from aiogram import Bot

from .config import TelegramConfig


def create_bot(config: TelegramConfig) -> Bot:
    bot = Bot(config.telegram_bot_token)
    return bot
