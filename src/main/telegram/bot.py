from aiogram import Bot

from .config import Config


def create_bot(config: Config) -> Bot:
    bot = Bot(config.bot_token)
    return bot
