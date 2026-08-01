import logging
import asyncio
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from tg_bot.handlers import get_handlers_routers

import tg_bot.config as config  # Settings

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
    dp.include_router(get_handlers_routers())

    try:
        # Ignore message sent before polling
        await bot.delete_webhook(drop_pending_updates=True)
        # Start bot's polling
        await dp.start_polling(bot)

    except Exception as error:
        logging.error(f"Error in starting bot polling: {error}")

    finally:
        await bot.session.close()


def main():
    """A little hack for uv to better work"""
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("Bot turned off")


if __name__ == "__main__":
    main()
