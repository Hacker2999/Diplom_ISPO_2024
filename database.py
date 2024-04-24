from models import User, Schedule, TeacherSchedule  # Импорт моделей из вашего проекта


def get_user(user_id):
    """Получить информацию о пользователе по его ID."""
    try:
        user = User.get(User.user_id == user_id)
        return user
    except User.DoesNotExist:
        return None


def create_user(user_id, department, course, group_number):
    """Создать новую запись о пользователе."""
    user = User(user_id=user_id, department=department, course=course, group_number=group_number)
    user.save()
    return user


def get_schedule_for_group(group_number, day=None):
    """Получить расписание для определенной группы и, при необходимости, отфильтровать по дню."""
    query = Schedule.select().where(Schedule.group_number == group_number)
    if day:
        query = query.where(Schedule.day == day)
    return list(query)


def get_schedules_for_teacher(teacher_name, day=None):
    """Получить расписание для определенного преподавателя и, при необходимости, отфильтровать по дню."""
    query = TeacherSchedule.select().where(TeacherSchedule.teacher_name == teacher_name)
    if day:
        query = query.where(TeacherSchedule.day == day)
    return list(query)


def get_courses_for_department(department_name, day=None):
    """Получить курсы для определенного отделения и, при необходимости, отфильтровать по дню."""
    query = TeacherSchedule.select().where(TeacherSchedule.teacher_name == department_name)
    if day:
        query = query.where(TeacherSchedule.day == day)
    return list(query)


def get_groups_for_department_and_course(department_name, day=None):
    """Получить группы для определенного отделения и курса и, при необходимости, отфильтровать по дню."""
    query = TeacherSchedule.select().where(TeacherSchedule.teacher_name == department_name)
    if day:
        query = query.where(TeacherSchedule.day == day)
    return list(query)


def get_users_by_group(group_number):
    """Получает список пользователей по номеру группы."""
    users = User.select().where(User.group_number == group_number)
    return list(users)


def get_user_by_id(user_id):
    """Get user information by user ID."""
    try:
        user = User.get(User.user_id == user_id)
        return user
    except User.DoesNotExist:
        return None


def get_user_schedule(group_number):
    """Get the schedule for a specific group."""
    try:
        schedule = Schedule.select().where(Schedule.group_number == group_number)
        return list(schedule)
    except Schedule.DoesNotExist:
        return None


def get_teacher_schedule(teacher_name):
    """Get the schedule for a specific teacher."""
    try:
        schedule = TeacherSchedule.select().where(TeacherSchedule.teacher_name == teacher_name)
        return list(schedule)
    except TeacherSchedule.DoesNotExist:
        return None
