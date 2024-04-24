from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from models import User


class Registration(StatesGroup):
    department = State()
    course = State()
    group_number = State()


async def start(message: types.Message):
    await message.answer("Добро пожаловать! Нажмите /register для начала регистрации или /help для справки.")


async def help(message: types.Message):
    help_text = (
        "Доступные команды:\n"
        "/register - Начать регистрацию\n"
        "/schedule - Просмотр расписания"
    )
    await message.answer(help_text)


async def register(message: types.Message, state: FSMContext):
    await message.answer("Выберите ваше отделение:")
    await Registration.department.set()


async def register_department(message: types.Message, state: FSMContext):
    department = message.text
    await state.update_data(department=department)
    await message.answer("Выберите ваш курс:")
    await Registration.course.set()


async def register_course(message: types.Message, state: FSMContext):
    course = message.text
    await state.update_data(course=course)
    await message.answer("Введите номер вашей группы:")
    await Registration.group_number.set()


async def register_group_number(message: types.Message, state: FSMContext):
    group_number = message.text
    await state.update_data(group_number=group_number)
    user_data = await state.get_data()

    # Получаем данные пользователя из состояния
    user_id = message.from_user.id
    department = user_data.get('department')
    course = user_data.get('course')

    # Создаем запись пользователя в базе данных
    user = User.create(user_id=user_id, department=department, course=course, group_number=group_number)

    # Проверяем успешность создания записи
    if user:
        print("Пользователь успешно создан.")
    else:
        print("Ошибка при создании пользователя.")

    await message.answer("Регистрация завершена!")
    await state.finish()



def register_handlers(dp):
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(help, commands="help")
    dp.register_message_handler(register, commands="register", state=None)
    dp.register_message_handler(register_department, state=Registration.department)
    dp.register_message_handler(register_course, state=Registration.course)
    dp.register_message_handler(register_group_number, state=Registration.group_number)
