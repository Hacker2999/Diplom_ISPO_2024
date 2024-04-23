import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import BOT_TOKEN

# Configure logging (optional)
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Register middlewares (optional)
dp.middleware.setup(LoggingMiddleware())

# Import and register handlers
from handlers import register_handlers
register_handlers(dp)

# Start the bot
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)