import pytest
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from config import BOT_TOKEN  # Assuming you have your bot token in config.py

# Define a fixture to create a bot instance
@pytest.fixture
async def bot():
    bot = Bot(token=BOT_TOKEN)
    yield bot
    await bot.close()

# Define a fixture to create a dispatcher
@pytest.fixture
async def dp(bot):
    dp = Dispatcher(bot)
    yield dp

# Define fixtures for specific modules or components as needed
# For example, a fixture to set up and tear down database connections

# ... (Add more fixtures as required)