from aiogram import types
from aiogram.dispatcher import FSMContext

from commands import Registration  # Import the StatesGroup from commands.py
from database import get_courses_for_department, get_groups_for_department_and_course
from main import dp


@dp.message_handler(state=Registration.department)
async def register_department(message: types.Message, state: FSMContext):
    department = message.text
    # Add validation for department (optional)
    await state.update_data(department=department)

    # Implement logic to get available courses for the selected department
    courses = get_courses_for_department(department)  # Replace with your implementation

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for course in courses:
        keyboard.add(types.KeyboardButton(text=course))
    await message.answer("Choose your course:", reply_markup=keyboard)
    await state.set_state(Registration.course)


@dp.message_handler(state=Registration.course)
async def register_course(message: types.Message, state: FSMContext):
    course = message.text
    # Add validation for course (optional)
    await state.update_data(course=course)

    # Implement logic to get available groups for the selected department and course
    groups = get_groups_for_department_and_course(state.get_data())  # Replace with your implementation

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for group in groups:
        keyboard.add(types.KeyboardButton(text=group))
    await message.answer("Choose your group number:", reply_markup=keyboard)
    await state.set_state(Registration.group_number)