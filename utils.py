
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import locale
from models import Subjects, Teachers, Classrooms, Groups, GroupsToTimetable, Timetable
from logs import logger
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
        group_to_timetable = GroupsToTimetable.filter(GroupsToTimetable.B == item.id).get()
        group = group_to_timetable.A
        group_name = group.name
        subgroup = ""
        if " п/г 1" in group_name:
            subgroup = " п/г 1"
        elif " п/г 2" in group_name:
            subgroup = " п/г 2"

        if day not in day_items:
            day_items[day] = set()
        day_items[day].add((item.lesson_number, subject, teacher, classroom, subgroup))

    # Sort the days in ascending order
    sorted_days = sorted(day_items.keys(), key=lambda x: datetime.strptime(x, "%d.%m/%A"))

    for day in sorted_days:
        output += f"{day}\n"
        for item in sorted(list(day_items[day])):
            output += f"{item[0]} - {item[1]} ({item[2]}){item[4]}\nКаб: {item[3]}\n"
        output += "\n"

    logger.debug("Exiting format_schedule function")
    return output

def format_teacher_schedule(schedule_data):
    output = ""
    day_items = {}
    for item in schedule_data:
        date = item.date
        day = date.strftime("%d.%m/%A")  # Extract the day of the week (e.g., Monday, Tuesday, etc.)
        subject_id = item.subjectId
        subject = Subjects.get(id=subject_id).name
        classroom_id = item.classroomId
        classroom = Classrooms.get(id=classroom_id).name
        group_to_timetable = GroupsToTimetable.filter(GroupsToTimetable.B == item.id).get()
        group = group_to_timetable.A
        group_name = group.name

        if day not in day_items:
            day_items[day] = set()
        day_items[day].add((item.lesson_number, subject, group_name, classroom))

    # Sort the days in ascending order
    sorted_days = sorted(day_items.keys(), key=lambda x: datetime.strptime(x, "%d.%m/%A"))

    # Format the output
    for day in sorted_days:
        output += f"{day}\n"
        for item in sorted(day_items[day]):
            output += f"{item[0]} - {item[1]} ({item[2]})\nКаб: {item[3]}\n"
        output += "\n"

    return output
def group_schedule_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        "Моё расписание",
        "Поиск расписания"
    )
    return keyboard
