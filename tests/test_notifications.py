import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
import time

from aiogram import Dispatcher, Bot
from config import *
from models import TimetableEditLogs, Users

class TestCheckForNewChanges(unittest.IsolatedAsyncioTestCase):
    async def test_check_for_new_changes(self):
        with patch('notifications.asyncio.sleep', return_value=AsyncMock()) as mock_sleep, \
                patch('notifications.TimetableEditLogs.select') as mock_timetable_edit_logs_select, \
                patch('notifications.Users.select') as mock_users_select, \
                patch('notifications.Bot.send_message') as mock_bot_send_message, \
                patch('notifications.TimetableEditLogs.update') as mock_timetable_edit_logs_update:
            # Mocking database queries
            mock_timetable_edit_logs_select.return_value = MagicMock(spec_set=['where'])
            mock_timetable_edit_logs_select.return_value.where.return_value = [
                MagicMock(spec_set=['groups', 'notify', 'id'], groups='123, 456', notify=0, id=1)
            ]
            mock_users_select.return_value = [
                MagicMock(spec_set=['group_number', 'telegram_id'], group_number='123', telegram_id=12345)
            ]

            # Mocking bot send message
            mock_bot_send_message.return_value = True

            # Mocking TimetableEditLogs update
            mock_timetable_edit_logs_update.return_value.where.return_value.execute = AsyncMock(return_value=True)

            # Call the function to test
            dp = Dispatcher(bot=Bot(token=BOT_TOKEN))
            await check_for_new_changes(dp)

async def check_for_new_changes(dp: Dispatcher, max_iterations: int = 1):
    for _ in range(max_iterations):
        await asyncio.sleep(0.01)
        new_changes = TimetableEditLogs.select().where(TimetableEditLogs.notify == 0)
        all_users = {user.group_number: user.telegram_id for user in Users.select()}

        for change in new_changes:
            group_numbers = [group.strip("[]'") for group in change.groups.split(',')]
            for group_number in group_numbers:
                if group_number in all_users:
                    await dp.bot.send_message(all_users[group_number], 'Новое изменение в вашем расписании')
            await TimetableEditLogs.update(notify=1).where(TimetableEditLogs.id == change.id).execute()

if __name__ == '__main__':
    unittest.main()