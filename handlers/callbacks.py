from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database import get_teacher_schedule, get_schedule, get_teachers_by_surname
from models import Users
from utils import format_schedule, format_teacher_schedule
from logs import logger


async def group_schedule(callback_query: types.CallbackQuery, bot):
    logger.info(f"User {callback_query.from_user.id} clicked 'Group Schedule' button")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Моё расписание")
    button2 = KeyboardButton("Поиск расписания")
    keyboard.row(button1, button2)
    await bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup=keyboard)


async def search_schedule(message: types.Message, bot):
    logger.info(f"User {message.from_user.id} sent message: {message.text}")
    if message.text == "Назад":
        await group_schedule(message, bot)
    else:
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton("Поиск по группе")
        button2 = KeyboardButton("Поиск по преподавателю")
        button3 = KeyboardButton("Назад")
        keyboard.row(button1, button2)
        keyboard.add(button3)
        await message.answer("Выберите способ поиска:", reply_markup=keyboard)


async def ask_group_number(message: types.Message, bot):
    logger.info(f"User {message.from_user.id} sent message: {message.text}")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Назад")
    keyboard.add(button)
    await message.answer("Введите номер группы в формате 'XXXXX/X', например: 42928/2", reply_markup=keyboard)


async def search_schedule_by_group(message: types.Message, bot):
    logger.info(f"User {message.from_user.id} sent message: {message.text}")
    if message.text == "Назад":
        await search_schedule(message, bot)
    else:
        group_number = message.text
        schedule = await get_schedule(group_number)
        if schedule:
            formatted_schedule = format_schedule(schedule)
            await message.answer(formatted_schedule, parse_mode="html")
            # Send new message with group_schedule buttons
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = KeyboardButton("Моё расписание")
            button2 = KeyboardButton("Поиск расписания")
            keyboard.row(button1, button2)
            await message.answer("Выберите действие:", reply_markup=keyboard)
        else:
            await message.answer("Расписание для указанной группы не найдено.")


async def handle_search_group(message: types.Message, bot):
    await ask_group_number(message, bot)


async def my_schedule(message: types.Message, bot):
    logger.info(f"User {message.from_user.id} sent message: {message.text}")
    user_id = message.from_user.id
    try:
        user = Users.get(telegram_id=user_id)
        if user:
            if user.teacher_role == 0:  # Student
                group_number = user.group_number
                schedule = await get_schedule(group_number)
                if schedule:
                    formatted_schedule = format_schedule(schedule)
                    await message.answer(formatted_schedule, parse_mode="html")
                    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
                    button1 = KeyboardButton("Моё расписание")
                    button2 = KeyboardButton("Поиск расписания")
                    keyboard.row(button1, button2)
                    await message.answer("Выберите действие:", reply_markup=keyboard)
                else:
                    await message.answer("Расписание для вашей группы не найдено.")
            else:  # Teacher
                teacher_name = user.teacher_lastname
                schedule = await get_teacher_schedule(teacher_name)
                if schedule:
                    formatted_schedule = format_teacher_schedule(schedule)
                    await message.answer(formatted_schedule, parse_mode="html")
                    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
                    button1 = KeyboardButton("Моё расписание")
                    button2 = KeyboardButton("Поиск расписания")
                    keyboard.row(button1, button2)
                    await message.answer("Выберите действие:", reply_markup=keyboard)
                else:
                    await message.answer("Расписание для указанного преподавателя не найдено.")
        else:
            await message.answer("Вашего пользователя нет в базе данных.")
    except Users.DoesNotExist:
        await message.answer("Вашего пользователя нет в базе данных.")
    except Exception as e:
        logger.error(f"Error fetching schedule for user {user_id}: {e}")
        await message.answer("Произошла ошибка при получении расписания.")


async def ask_teacher_surname(message: types.Message, bot):
    logger.info(f"User {message.from_user.id} sent message: {message.text}")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton("Назад")
    keyboard.add(button)
    await message.answer("Введите фамилию преподавателя:", reply_markup=keyboard)


async def search_teacher_surname(message: types.Message, bot):
    logger.info(f"User {message.from_user.id} sent message: {message.text}")
    if message.text == "Назад":
        await search_schedule(message, bot)
    else:
        surname = message.text
        teachers = get_teachers_by_surname(surname)  # new function to get teachers by surname
        if teachers:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            for teacher in teachers:
                button = KeyboardButton(teacher.name)
                keyboard.add(button)
            await message.answer("Выберите преподавателя:", reply_markup=keyboard)
        else:
            await message.answer("Преподаватели с такой фамилией не найдены.")


async def select_teacher(message: types.Message, bot):
    logger.info(f"User {message.from_user.id} sent message: {message.text}")
    teacher_name = message.text
    schedule = await get_teacher_schedule(teacher_name)
    if schedule:
        formatted_schedule = format_teacher_schedule(schedule)
        await message.answer(formatted_schedule, parse_mode="html")

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton("Моё расписание")
        button2 = KeyboardButton("Поиск расписания")
        keyboard.row(button1, button2)
        await message.answer("Выберите действие:", reply_markup=keyboard)
    else:
        await message.answer("Расписание для указанного преподавателя не найдено.")


async def handle_back(message: types.Message, bot):
    logger.info(f"User {message.from_user.id} sent message: {message.text}")
    previous_message_text = message.text
    if previous_message_text == "Выберите способ поиска:":
        await search_schedule(message, bot)
    else:
        await group_schedule(message, bot)


def register_callbacks(dp, bot):
    dp.register_callback_query_handler(group_schedule, text="group_schedule")
    dp.register_callback_query_handler(my_schedule, text="my_schedule")

    dp.register_message_handler(lambda message: search_schedule(message, bot),
                                lambda message: message.text == "Поиск расписания")
    dp.register_message_handler(lambda message: ask_group_number(message, bot),
                                lambda message: message.text.isdigit() and len(message.text) == 6)

    dp.register_message_handler(lambda message: search_schedule_by_group(message, bot),
                                lambda message: message.text.count('/') == 1 and message.text not in ["Назад",
                                                                                                      "Моё расписание",
                                                                                                      "Поиск расписания",
                                                                                                      "Поиск по группе",
                                                                                                      "Поиск по преподавателю"])
    dp.register_message_handler(lambda message: my_schedule(message, bot),
                                lambda message: message.text == "Моё расписание")
    dp.register_message_handler(lambda message: ask_teacher_surname(message, bot),
                                lambda message: message.text == "Поиск по преподавателю")

    dp.register_message_handler(lambda message: search_teacher_surname(message, bot),
                                lambda message: message.text.isalpha() and len(message.text) > 3)

    dp.register_message_handler(lambda message: select_teacher(message, bot),
                                lambda message: message.text not in ["Назад", "Моё расписание", "Поиск расписания",
                                                                     "Поиск по группе", "Поиск по преподавателю"])

    dp.register_message_handler(lambda message: handle_back(message, bot), lambda message: message.text == "Назад")
    dp.register_message_handler(lambda message: handle_search_group(message, bot),
                                lambda message: message.text == "Поиск по группе")

