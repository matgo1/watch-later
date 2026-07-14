import logging
import asyncio
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

import tg_bot.config as config

logger = logging.getLogger(__name__)  # Collect logs


async def run_bot():
    logger.info("Initializing Telegram Bot")


def main():
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("Bot turned off")


if __name__ == "__main__":
    main()
