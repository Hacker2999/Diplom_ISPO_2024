from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import create_user, update_user
from handlers.messages import *
from models import Users
from logs import logger

class Registration(StatesGroup):
    role = State()
    group_number_or_teacher_lastname = State()

class ChangeInfo(StatesGroup):
    new_info = State()

async def start(message: types.Message):
    logger.info(f"User {message.from_user.id} sent /start command")
    await message.answer(START_MESSAGE)

async def help(message: types.Message):
    logger.info(f"User {message.from_user.id} sent /help command")
    await message.answer(HELP_MESSAGE)

async def register(message: types.Message, state: FSMContext):
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
        await message.answer("Введите номер группы:")
        await Registration.group_number_or_teacher_lastname.set()
    elif role == "Учитель":
        await message.answer("Введите фамилию:")
        await Registration.group_number_or_teacher_lastname.set()

async def register_group_number_or_teacher_lastname(message: types.Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} sent group number or teacher lastname: {message.text}")
    user_data = await state.get_data()
    role = user_data.get('role')
    user_id = message.from_user.id
    if role == "Студент":
        group_number = message.text
        user = create_user(
            telegram_id=user_id,
            group_number=group_number
        )
    elif role == "Учитель":
        teacher_lastname = message.text
        user = create_user(
            telegram_id=user_id,
            teacher_lastname=teacher_lastname,
            teacher_role=1
        )

    if user:
        logger.info(f"User {user_id} successfully created")
        print("Пользователь успешно создан.")
    else:
        logger.error(f"Error creating user {user_id}")
        print("Ошибка при создании пользователя.")

    # Создаем inline-клавиатуру
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Моё расписание", "Поиск расписания")

    # Отправляем сообщение с inline-клавиатурой
    await message.answer(REGISTRATION_COMPLETE_MESSAGE, reply_markup=keyboard)
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
    dp.register_message_handler(help, commands="help")
    dp.register_message_handler(register, commands="register", state=None)
    dp.register_message_handler(register_role, state=Registration.role)
    dp.register_message_handler(register_group_number_or_teacher_lastname, state=Registration.group_number_or_teacher_lastname)
    dp.register_message_handler(change_info, commands="change_info", state=None)
    dp.register_message_handler(change_info_new_info, state=ChangeInfo.new_info)