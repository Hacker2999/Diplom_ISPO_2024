from models import User, Schedule, TeacherSchedule  # Import your models


def get_user(user_id):
    """Get user information by user ID."""
    try:
        user = User.get(User.user_id == user_id)
        return user
    except User.DoesNotExist:
        return None


def create_user(user_id, department, course, group_number):
    """Create a new user record."""
    user = User(user_id=user_id, department=department, course=course, group_number=group_number)
    user.save()
    return user


def get_schedule_for_group(group_number, day=None):
    """Get the schedule for a specific group and optionally filter by day."""
    query = Schedule.select().where(Schedule.group_number == group_number)
    if day:
        query = query.where(Schedule.day == day)
    return list(query)


def get_schedules_for_teacher(teacher_name, day=None):
    """Get schedules for a specific teacher and optionally filter by day."""
    query = TeacherSchedule.select().where(TeacherSchedule.teacher_name == teacher_name)
    if day:
        query = query.where(TeacherSchedule.day == day)
    return list(query)


def get_courses_for_department(department_name, day=None):
    """Get schedules for a specific teacher and optionally filter by day."""
    query = TeacherSchedule.select().where(TeacherSchedule.teacher_name == department_name)
    if day:
        query = query.where(TeacherSchedule.day == day)
    return list(query)


def get_groups_for_department_and_course(department_name, day=None):
    """Get schedules for a specific teacher and optionally filter by day."""
    query = TeacherSchedule.select().where(TeacherSchedule.teacher_name == department_name)
    if day:
        query = query.where(TeacherSchedule.day == day)
    return list(query)

# ... (Add other database interaction functions as needed)
