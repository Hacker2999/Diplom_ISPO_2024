from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import locale
from middlewares import logger
from models import Subjects, Teachers, Classrooms


locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"  # Note: do not use "de_DE" as it doesn't work
)


def format_schedule(schedule_data):
    logger.debug("Entering format_schedule function")
    output = ""
    day_items = {}
    for item in schedule_data:
        logger.debug("Processing item: %s", item)
        date = item.date
        day = date.strftime("%d.%m/%A")  # Extract the day of the week (e.g., Monday, Tuesday, etc.)
        logger.debug("Extracted day: %s", day)
        subject_id = item.subjectId
        subject = Subjects.get(id=subject_id).name
        logger.debug("Retrieved subject name: %s", subject)
        teacher_id = item.teacherId
        teacher = Teachers.get(id=teacher_id).name
        logger.debug("Retrieved teacher name: %s", teacher)
        classroom_id = item.classroomId
        classroom = Classrooms.get(id=classroom_id).name
        logger.debug("Retrieved classroom name: %s", classroom)

        # Group items by day
        if day not in day_items:
            day_items[day] = []
        day_items[day].append((subject, teacher, classroom))

    # Sort the day_items dictionary by key (i.e., the date)
    sorted_days = sorted(day_items.keys())

    # Format the output
    for day in sorted_days:
        output += f"**{day}**\n"
        for subject, teacher, classroom in day_items[day]:
            output += f"{subject} ({teacher})\nКаб: {classroom}\n"
        output += "\n"

    logger.debug("Exiting format_schedule function")
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
