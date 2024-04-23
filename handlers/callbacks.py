from aiogram import types
from aiogram.dispatcher import FSMContext

from database import get_schedule_for_group
from main import dp
from utils import format_schedule  # Assuming you have a utility function for formatting


@dp.callback_query_handler(text="my_schedule")
async def show_my_schedule(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    user_data = await state.get_data()
    if not user_data:
        await callback_query.message.answer("Please register first!")
        return

    group_number = user_data['group_number']
    schedule = get_schedule_for_group(group_number)  # Replace with your implementation

    if schedule:
        formatted_schedule = format_schedule(schedule)
        await callback_query.message.answer(formatted_schedule)
    else:
        await callback_query.message.answer("No schedule found for your group.")


@dp.callback_query_handler(text_startswith="group_")
async def show_group_schedule(callback_query: types.CallbackQuery):
    group_number = callback_query.data.split("_")[1]
    schedule = get_schedule_for_group(group_number)  # Replace with your implementation

    if schedule:
        formatted_schedule = format_schedule(schedule)
        await callback_query.message.answer(formatted_schedule)
    else:
        await callback_query.message.answer("No schedule found for this group.")

# ... Implement similar handlers for other callback actions (e.g., teacher schedule)