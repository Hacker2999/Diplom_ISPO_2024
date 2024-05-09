import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import register_handlers, register_callbacks
from aiogram import executor
from logs import setup_logging
from notifications import check_for_new_changes

# Setup logging
logger = setup_logging(log_level=logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def on_startup(dp: Dispatcher):
    logger.info("Bot started")
    asyncio.create_task(check_for_new_changes(dp))

# Register handlers and callbacks
register_handlers(dp)
register_callbacks(dp, bot)

# Start the bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)