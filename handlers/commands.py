from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from peewee import DatabaseError
from database import create_user, update_user, get_teachers_by_surname
from handlers.messages import *
from models import Users, Teachers
from logs import logger


class Registration(StatesGroup):
    teacher_select = State()
    role = State()
    group_number = State()
    teacher_lastname = State()


class ChangeInfo(StatesGroup):
    new_info = State()


async def start(message: types.Message):
    logger.info(f"User {message.from_user.id} sent /start command")
    user_id = message.from_user.id
    try:
        user = Users.get(telegram_id=user_id)
    except Users.DoesNotExist:
        # User doesn't exist, show registration button
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Регистрация")
        await message.answer(START_MESSAGE, reply_markup=keyboard)
    else:
        # User already exists, show schedule buttons
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Моё расписание", "Поиск расписания")
        await message.answer("С возвращением!", reply_markup=keyboard)


async def register_button(message: types.Message):
    logger.info(f"User {message.from_user.id} pressed register button")
    await register(message)


async def register(message: types.Message):
    logger.info(f"User {message.from_user.id} sent /register command")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Студент", "Учитель")
    await message.answer("Выберите роль:", reply_markup=keyboard)
    await Registration.role.set()


async def register_role(message: types.Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} sent role: {message.text}")
    role = message.text
    await state.update_data(role=role)

    if role == "Студент":
        await message.answer("Введите номер группы:", reply_markup=types.ReplyKeyboardRemove())
        await Registration.group_number.set()
    elif role == "Учитель":
        await message.answer("Введите фамилию:", reply_markup=types.ReplyKeyboardRemove())
        await Registration.teacher_lastname.set()  # Set the teacher_lastname state explicitly


async def register_group_number(message: types.Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} sent group number: {message.text}")
    user_data = await state.get_data()
    role = user_data.get('role')
    user_id = message.from_user.id
    group_number = message.text

    try:
        user = create_user(
            telegram_id=user_id,
            group_number=group_number
        )
        if user:
            logger.info(f"User {user_id} successfully created")
            await message.answer("Пользователь успешно создан.")
        else:
            logger.error(f"Error creating user {user_id}")
            await message.answer("Ошибка при создании пользователя.")
    except Exception as e:
        logger.error(f"Error creating user {user_id}: {e}")
        await message.answer("Произошла ошибка при создании пользователя.")


async def register_teacher_lastname(message: types.Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} sent teacher lastname: {message.text}")
    user_data = await state.get_data()
    role = user_data.get('role')
    user_id = message.from_user.id
    teacher_lastname = message.text

    logger.info(f"Current state: {await state.get_state()}")
    try:
        teachers = get_teachers_by_surname(teacher_lastname)
        if teachers:
            # Store the list of teacher names in the state
            await state.update_data(teachers=[str(teacher.name) for teacher in teachers])
            # Create a keyboard with the teacher names
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for teacher in teachers:
                keyboard.add(str(teacher.name))
            await message.answer("Выберите фамилию:", reply_markup=keyboard)
            await Registration.teacher_select.set()  # Set the teacher_select state explicitly
            logger.info(f"Next state: {await state.get_state()}")
        else:
            await message.answer(
                "Учителя с такой фамилией не найдено. Попробуйте снова.")
    except Exception as e:
        logger.error(f"Error retrieving teachers: {e}")
        await message.answer(f"Произошла ошибка при получении списка учителей: {e}")
        await state.finish()
        return


async def register_teacher_select(message: types.Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} selected teacher: {message.text}")
    user_data = await state.get_data()
    role = user_data.get('role')
    user_id = message.from_user.id
    selected_teacher = message.text

    try:
        logger.info("Getting teachers from state data...")
        teachers = user_data.get('teachers')
        if selected_teacher in teachers:
            logger.info("Selected teacher is in the list...")
            # Get the teacher ID from the database
            teacher = Teachers.select().where(Teachers.name == selected_teacher).first()
            teacher_id = teacher.id

            logger.info("Creating new user...")
            # Create a new user with the selected teacher
            user = create_user(
                telegram_id=user_id,
                teacher_lastname=selected_teacher,
                teacher_role=1
            )
            user.save()

            logger.info(f"User {user_id} created successfully with teacher {selected_teacher}")
            await message.answer("Вы успешно зарегистрировались как учитель!", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add("Моё расписание", "Поиск расписания"))
            await state.finish()
        else:
            await message.answer("Выберите фамилию из списка.")
    except DatabaseError as e:
        logger.error(f"Database error creating user: {e}")
        await message.answer(f"Произошла ошибка при создании пользователя: {e}")
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        await message.answer(f"Произошла ошибка при создании пользователя: {e}")
    finally:
        await state.finish()


async def change_info(message: types.Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} sent /change_info command")
    user_id = message.from_user.id
    user = Users.get(telegram_id=user_id)
    if user.teacher_role == 0:  # Student
        await message.answer("Введите новый номер группы:")
    else:  # Teacher
        await message.answer("Введите новую фамилию:")
    await ChangeInfo.new_info.set()


async def change_info_new_info(message: types.Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} sent new info: {message.text}")
    user_id = message.from_user.id
    user = Users.get(telegram_id=user_id)
    if user.teacher_role == 0:  # Student
        new_group_number = message.text
        if update_user(user_id, group_number=new_group_number):
            logger.info(f"User {user_id} group number updated successfully")
            await message.answer(GROUP_NUMBER_UPDATED_MESSAGE)
        else:
            logger.error(f"Error updating user {user_id} group number")
            await message.answer(GROUP_NUMBER_UPDATE_ERROR_MESSAGE)
    else:  # Teacher
        new_teacher_lastname = message.text
        if update_user(user_id, teacher_lastname=new_teacher_lastname):
            logger.info(f"User {user_id} teacher lastname updated successfully")
            await message.answer(TEACHER_LASTNAME_UPDATED_MESSAGE)
        else:
            logger.error(f"Error updating user {user_id} teacher lastname")
            await message.answer(TEACHER_LASTNAME_UPDATE_ERROR_MESSAGE)
    await state.finish()


def register_handlers(dp):
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(register_button, text="Регистрация")
    dp.register_message_handler(register, commands="register", state=None)
    dp.register_message_handler(register_role, state=Registration.role)
    dp.register_message_handler(register_group_number, state=Registration.group_number)
    dp.register_message_handler(register_teacher_lastname, state=Registration.teacher_lastname)
    dp.register_message_handler(register_teacher_select, state=Registration.teacher_select)
    dp.register_message_handler(change_info, commands="change_info", state=None)
    dp.register_message_handler(change_info_new_info, state=ChangeInfo.new_info)
