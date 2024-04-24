from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import BOT_TOKEN
from handlers import register_handlers, register_callbacks
from aiogram import executor

from logs import setup_logging

setup_logging()

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Регистрация мидлваров (по желанию)
dp.middleware.setup(LoggingMiddleware())

# Регистрация обработчиков команд и коллбэков
register_handlers(dp)
register_callbacks(dp, bot)

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
