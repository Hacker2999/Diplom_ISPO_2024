from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def format_schedule(schedule_data):
    """Функция для форматирования расписания."""
    output = ""
    for item in schedule_data:
        day = item['day']
        time = item['time']
        subject = item['subject']
        teacher = item['teacher']
        room = item['room'] if item.get('room') else "N/A"
        output += f"**{day}**  {time}\n{subject} ({teacher})\nRoom: {room}\n\n"
    return output


def get_current_weekday():
    """Функция для получения текущего дня недели."""
    return datetime.today().strftime("%A")


def group_schedule_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Моё расписание", callback_data="my_schedule"),
        InlineKeyboardButton(text="Поиск расписания", callback_data="search_schedule")
    )
    return keyboard
