from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from logs import logger  # Import the logger from the logs file

class LoggingMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        logger.debug("Received update: %s", update)
        logger.debug("Starting to process update...")

    async def on_process_update(self, update: types.Update, data: dict):
        logger.debug("Processing update: %s", update)

    async def on_post_process_update(self, update: types.Update, data: dict):
        logger.debug("Finished processing update: %s", update)

    async def on_send_message(self, message: types.Message):
        logger.debug("Sending message: %s", message)

    async def on_receive_message(self, message: types.Message):
        logger.debug("Received message: %s", message)

class ErrorHandlerMiddleware(BaseMiddleware):
    async def on_error(self, update: types.Update, error, data: dict):
        logger.error("An error occurred: %s", error)
        logger.debug("Error details: %s", error.__dict__)
        await update.message.answer("An error occurred. Please try again later.")
        return True  # Prevent further processing