import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import register_handlers, register_callbacks
from aiogram import executor

from notifications import check_for_new_changes

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def on_startup(dp: Dispatcher):
    asyncio.create_task(check_for_new_changes(dp))

# Регистрация обработчиков команд и коллбэков
register_handlers(dp)
register_callbacks(dp, bot)

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
