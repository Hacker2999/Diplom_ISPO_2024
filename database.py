import datetime
from logs import logger
from models import Users, Timetable, Teachers, Groups, Classrooms, GroupsToTimetable, Subjects



def get_user_by_id(user_id):
    try:
        user = Users.get(Users.id == user_id)
        logger.info(f"User {user_id} found in database")
        return user
    except Users.DoesNotExist:
        logger.info(f"User {user_id} not found in database")
        return None

def create_user(telegram_id, **kwargs):
    try:
        user = Users.create(
            telegram_id=telegram_id,
            **kwargs
        )
        logger.info(f"User {telegram_id} created successfully")
        return user
    except Exception as e:
        logger.error(f"Error creating user {telegram_id}: {e}")
        return None

def update_user(telegram_id, **kwargs):
    try:
        user = Users.get(telegram_id=telegram_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            user.save()
            logger.info(f"User {telegram_id} updated successfully")
            return True
        logger.info(f"User {telegram_id} not found in database")
        return False
    except Exception as e:
        logger.error(f"Error updating user {telegram_id}: {e}")
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

        result = query.execute()
        logger.info(f"Schedule for group {group_number} retrieved successfully")
        return result
    except Exception as e:
        logger.error(f"Error retrieving schedule for group {group_number}: {e}")
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

        result = query.execute()
        logger.info(f"Schedule for teacher {teacher_surname} retrieved successfully")
        return result
    except Exception as e:
        logger.error(f"Error retrieving schedule for teacher {teacher_surname}: {e}")
        return None