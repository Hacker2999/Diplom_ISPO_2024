import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        logger.info("Received update: %s", update)

    async def on_post_process_update(self, update: types.Update, data: dict):
        logger.info("Update processed successfully.")

class ErrorHandlerMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        if message.text == "error":
            raise ValueError("Intentional error")

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        if query.data == "error":
            raise ValueError("Intentional error")

    async def on_error(self, update: types.Update, error, data: dict):
        logger.exception("An error occurred: %s", error)
        await update.message.answer("An error occurred. Please try again later.")
        return True  # Prevent further processing
