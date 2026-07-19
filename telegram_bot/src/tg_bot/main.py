import logging
import asyncio
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

import tg_bot.config as config

logger = logging.getLogger(__name__)  # Collect logs


async def run_bot():
    logger.info("Initializing Telegram Bot")

    # Construct Bot
    bot = Bot(
        config.config.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Construct Dispatcher
    dp = Dispatcher()

    # Include routers
    # dp.include_router()

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    except Exception as error:
        logging.error(f"Error in starting bot polling: {error}")

    finally:
        await bot.session.close()


def main():
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("Bot turned off")


if __name__ == "__main__":
    main()
