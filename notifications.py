import asyncio
from aiogram import Bot, Dispatcher, executor, types

from config import BOT_TOKEN
from models import TimetableEditLogs, Users

bot = Bot(token=BOT_TOKEN)


async def check_for_new_changes(dp: Dispatcher):
    while True:
        await asyncio.sleep(1800)
        new_changes = TimetableEditLogs.select().where(TimetableEditLogs.notify == 0)
        all_users = {user.group_number: user.telegram_id for user in Users.select()}
        print("All users:", all_users)

        for change in new_changes:
            group_numbers = [group.strip("[]'") for group in change.groups.split(',')]
            print("Change groups:", group_numbers)
            users_to_notify = []
            for group_number in group_numbers:
                if group_number in all_users:
                    users_to_notify.append(all_users[group_number])
            print("Users to notify:", users_to_notify)
            for user in users_to_notify:
                try:
                    await dp.bot.send_message(user, f"Новое изменение в вашем расписании")
                except Exception as e:
                    print(f"Ошибка отправки сообщения пользователю {user}: {e}")

            try:
                TimetableEditLogs.update(notify=1).where(TimetableEditLogs.id == change.id).execute()
            except Exception as e:
                print(f"Ошибка обновления TimetableEditLogs: {e}")

