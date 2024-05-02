from aiogram import types
from database import get_user_schedule, get_teacher_schedule, get_user_by_id, get_users_by_group
from models import Users
from utils import format_schedule, group_schedule_keyboard


async def group_schedule(callback_query: types.CallbackQuery, bot):
    await bot.send_message(callback_query.from_user.id, "Выберите действие:", reply_markup=group_schedule_keyboard())


async def my_schedule(callback_query: types.CallbackQuery, bot):
    user_id = callback_query.from_user.id
    user = await get_user_by_id(user_id)
    if user:
        schedule = await get_user_schedule(user.group_number)
        if schedule:
            formatted_schedule = format_schedule(schedule)
            await bot.send_message(user_id, formatted_schedule)
        else:
            await bot.send_message(user_id, "Расписание для вашей группы не найдено.")
    else:
        await bot.send_message(user_id, "Вашего пользователя нет в базе данных.")


async def search_schedule(callback_query: types.CallbackQuery, bot):
    await bot.send_message(callback_query.from_user.id, "Введите номер группы для поиска расписания:")


async def search_schedule_by_group(message: types.Message, bot):
    user_id = message.from_user.id
    user = Users.get(telegram_id=user_id)
    group_number = user.group_number
    schedule = await get_user_schedule(group_number)
    if schedule:
        formatted_schedule = format_schedule(schedule)

        truncated_schedule = formatted_schedule[:4096]

        # Send the truncated text as a message
        await message.answer(truncated_schedule)


async def teacher_schedule(callback_query: types.CallbackQuery, bot):
    await bot.send_message(callback_query.from_user.id, "Введите фамилию преподавателя:")


async def search_schedule_by_teacher(message: types.Message, bot):
    teacher_name = message.text
    schedule = await get_teacher_schedule(teacher_name)
    if schedule:
        formatted_schedule = format_schedule(schedule)
        await message.answer(formatted_schedule)
    else:
        await message.answer("Расписание для указанного преподавателя не найдено.")
async def schedule_callback(callback_query: types.CallbackQuery, bot):
    if callback_query.data == "my_schedule":
        await my_schedule(callback_query, bot)
    elif callback_query.data == "search_schedule":
        await search_schedule(callback_query, bot)

def register_callbacks(dp, bot):
    dp.register_callback_query_handler(lambda c: group_schedule(c, bot), text="group_schedule")
    dp.register_callback_query_handler(lambda c: my_schedule(c, bot), text="my_schedule")
    dp.register_callback_query_handler(lambda c: search_schedule(c, bot), text="search_schedule")
    dp.register_message_handler(lambda m: search_schedule_by_group(m, bot), state=None)
    dp.register_callback_query_handler(lambda c: teacher_schedule(c, bot), text="teacher_schedule")
    dp.register_message_handler(lambda m: search_schedule_by_teacher(m, bot), state=None)
