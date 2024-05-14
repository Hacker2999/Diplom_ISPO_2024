
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import locale
from models import Subjects, Teachers, Classrooms, Groups, GroupsToTimetable, Timetable
from logs import logger
import html
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
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
            day_items[day] = {}
        if item.lesson_number not in day_items[day]:
            day_items[day][item.lesson_number] = []
        if (subject, teacher, classroom, subgroup) not in day_items[day][item.lesson_number]:
            day_items[day][item.lesson_number].append((subject, teacher, classroom, subgroup))

    # Sort the days in ascending order
    sorted_days = sorted(day_items.keys(), key=lambda x: datetime.strptime(x, "%d.%m/%A"))

    for day in sorted_days:
        output += f"<b>{html.escape(day)}</b>\n"
        for lesson_number in sorted(day_items[day].keys()):
            items = day_items[day][lesson_number]
            if len(items) > 1:
                output += f"{lesson_number}. "
                for i, item in enumerate(items):
                    output += f"<b>{html.escape(item[0])}</b> ({html.escape(item[1])}){html.escape(item[3])} - каб. {html.escape(item[2])}"
                    if i < len(items) - 1:
                        output += "\n    "
                output += "\n"
            else:
                output += f"{lesson_number}. <b>{html.escape(items[0][0])}</b> ({html.escape(items[0][1])}){html.escape(items[0][3])} - каб. {html.escape(items[0][2])}\n"
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
        subgroup = ""
        if " п/г 1" in group_name:
            subgroup = " п/г 1"
        elif " п/г 2" in group_name:
            subgroup = " п/г 2"

        if day not in day_items:
            day_items[day] = {}
        if item.lesson_number not in day_items[day]:
            day_items[day][item.lesson_number] = []
        if (subject, group_name, classroom, subgroup) not in day_items[day][item.lesson_number]:
            day_items[day][item.lesson_number].append((subject, group_name, classroom, subgroup))

    # Sort the days in ascending order
    sorted_days = sorted(day_items.keys(), key=lambda x: datetime.strptime(x, "%d.%m/%A"))

    for day in sorted_days:
        output += f"<b>{html.escape(day)}</b>\n"
        for lesson_number in sorted(day_items[day].keys()):
            items = day_items[day][lesson_number]
            if len(items) > 1:
                output += f"{lesson_number}. "
                for i, item in enumerate(items):
                    output += f"<b>{html.escape(item[0])}</b> ({html.escape(item[1])}){html.escape(item[3])} - каб. {html.escape(item[2])}"
                    if i < len(items) - 1:
                        output += "\n    "
                output += "\n"
            else:
                output += f"{lesson_number}. <b>{html.escape(items[0][0])}</b> ({html.escape(items[0][1])}){html.escape(items[0][3])} - каб. {html.escape(items[0][2])}\n"
        output += "\n"

    return output

