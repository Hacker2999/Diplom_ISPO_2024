from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from middlewares import logger
from models import Subjects, Teachers, Classrooms
from logs import setup_logging

setup_logging()

def format_schedule(schedule_data):
    """Функция для форматирования расписания."""
    logger.debug("Entering format_schedule function")
    output = ""
    for item in schedule_data:
        logger.debug("Processing item: %s", item)
        date = item.date
        day = date.strftime("%A")  # Extract the day of the week (e.g., Monday, Tuesday, etc.)
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
        output += f"**{day}**  \n{subject} ({teacher})\nRoom: {classroom}\n\n"
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

