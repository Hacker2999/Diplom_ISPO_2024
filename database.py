import datetime

from peewee import JOIN

from models import Users, Timetable, Teachers, Groups, Classrooms, GroupsToTimetable, Subjects


def get_user_by_id(user_id):
    try:
        user = Users.get(Users.id == user_id)
        return user
    except Users.DoesNotExist:
        return None


def create_user(telegram_id, username, first_name, last_name, department, course, group_number):
    user = Users.create(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        department=department,
        course=course,
        group_number=group_number
    )
    return user


def update_user(user_id, group_number):
    try:
        user = Users.get(Users.telegram_id == user_id)
        user.group_number = group_number
        user.save()
        return True
    except Users.DoesNotExist:
        return False


def get_schedule_for_group(group_name, day=None):
    query = Timetable.select().join(Groups).where(Groups.name == group_name)
    if day:
        query = query.where(Timetable.day == day)
    return list(query)


def get_schedules_for_teacher(teacher_name, day=None):
    query = Timetable.select().join(Teachers).where(Teachers.name == teacher_name)
    if day:
        query = query.where(Timetable.day == day)
    return list(query)


def get_courses_for_department(department_name, day=None):
    query = Groups.select().where(Groups.name == department_name)
    if day:
        query = query.where(Timetable.day == day)
    return list(query)


def get_groups_for_department_and_course(department_name, course_number, day=None):
    query = Groups.select().where(Groups.name == department_name, Groups.course == course_number)
    if day:
        query = query.where(Timetable.day == day)
    return list(query)


def get_users_by_group(group_name):
    users = Users.select().join(Groups).where(Groups.name == group_name)
    return list(users)


async def get_user_schedule(group_number):
    try:

        start_date = datetime.date(2024, 1, 20)
        end_date = datetime.date(2024, 1, 30)

        user = Users.get(group_number=group_number)
        subquery = (GroupsToTimetable
                    .select(GroupsToTimetable.B)
                    .join(Groups, on=(GroupsToTimetable.A == Groups.id))
                    .where(Groups.name == group_number))

        query = (Timetable
                 .select(Timetable, Teachers, Classrooms, Subjects, Groups)
                 .join(Teachers, on=(Timetable.teacherId == Teachers.id))
                 .join(Classrooms, on=(Timetable.classroomId == Classrooms.id))
                 .join(Subjects, on=(Timetable.subjectId == Subjects.id))
                 .join(GroupsToTimetable, on=(Timetable.id == GroupsToTimetable.B))
                 .join(Groups, on=(GroupsToTimetable.A == Groups.id))
                 .where(Timetable.date.between(start_date, end_date))
                 .where(Timetable.id << subquery)
                 .limit(60))

        return query.execute()
    except Exception as e:
        print("Ошибка при получении расписания пользователя:", e)
        return None


def get_teacher_schedule(teacher_name):
    try:
        schedule = Timetable.select().join(Teachers).where(Teachers.name == teacher_name)
        return list(schedule)
    except Timetable.DoesNotExist:
        return None
