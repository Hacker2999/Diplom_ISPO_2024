from main import dp  # Assuming your main bot logic is in main.py


async def test_start_command(bot, dp):
    # Send the /start command
    message = await bot.send_message(chat_id=..., text="/start")

    # Get updates from the dispatcher
    updates = await dp.get_updates()

    # Assert that the bot responded with the expected message
    assert updates[0].message.text == "Welcome!"