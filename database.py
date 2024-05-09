import datetime

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


async def get_schedule(group_number):
    try:
        start_date = datetime.date(2024, 5, 13)
        end_date = datetime.date(2024, 5, 25)

        subquery = (GroupsToTimetable
                    .select(GroupsToTimetable.B)
                    .join(Groups, on=(GroupsToTimetable.A == Groups.id))
                    .where((Groups.name == group_number) |
                           (Groups.name == f"{group_number} п/г 1") |
                           (Groups.name == f"{group_number} п/г 2")))

        query = (Timetable
                 .select(Timetable, Teachers, Classrooms, Subjects, Groups)
                 .join(Teachers, on=(Timetable.teacherId == Teachers.id))
                 .join(Classrooms, on=(Timetable.classroomId == Classrooms.id))
                 .join(Subjects, on=(Timetable.subjectId == Subjects.id))
                 .join(GroupsToTimetable, on=(Timetable.id == GroupsToTimetable.B))
                 .join(Groups, on=(GroupsToTimetable.A == Groups.id))
                 .where(Timetable.date.between(start_date, end_date))
                 .where(Timetable.id.in_(subquery))
                 .limit(60))

        return query.execute()
    except Exception as e:
        print("Ошибка при получении расписания пользователя:", e)
        return None


async def get_teacher_schedule(teacher_surname):
    try:
        start_date = datetime.date(2024, 5, 13)
        end_date = datetime.date(2024, 5, 25)

        subquery = (Timetable
                    .select(Timetable.id)
                    .join(Teachers, on=(Timetable.teacherId == Teachers.id))
                    .where(Teachers.name.contains(teacher_surname)))

        query = (Timetable
                 .select(Timetable, Teachers, Classrooms, Subjects, Groups)
                 .join(Teachers, on=(Timetable.teacherId == Teachers.id))
                 .join(Classrooms, on=(Timetable.classroomId == Classrooms.id))
                 .join(Subjects, on=(Timetable.subjectId == Subjects.id))
                 .join(GroupsToTimetable, on=(Timetable.id == GroupsToTimetable.B))
                 .join(Groups, on=(GroupsToTimetable.A == Groups.id))
                 .where(Timetable.date.between(start_date, end_date))
                 .where(Timetable.id.in_(subquery))
                 .limit(60))

        return query.execute()
    except Exception as e:
        print("Ошибка при получении расписания преподавателя:", e)
        return None
