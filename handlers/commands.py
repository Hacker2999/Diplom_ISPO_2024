from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# States for registration process
class Registration(StatesGroup):
    department = State()
    course = State()
    group_number = State()

def register_handlers(dp):
    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        await message.answer("Welcome Use /register to start registration or /help for more information.")

    @dp.message_handler(commands=["help"])
    async def help(message: types.Message):
        await message.answer("Available commands:\n/register - Start registration\n/schedule - View schedule")

    @dp.message_handler(commands=["register"], state=None)
    async def register_start(message: types.Message, state: FSMContext):
        await message.answer("Please choose your department:")
        # Implement department selection (e.g., using inline keyboard)
        await state.set_state(Registration.department)

    @dp.message_handler(state=Registration.department)
    async def register_department(message: types.Message, state: FSMContext):
        department = message.text
        await state.update_data(department=department)
        await message.answer("Choose your course:")
        await state.set_state(Registration.course)

    # ... Similar handlers for course and group_number

    @dp.message_handler(state=Registration.group_number)
    async def register_group_number(message: types.Message, state: FSMContext):
        group_number = message.text
        user_data = await state.get_data()
        user = User(user_id=message.from_user.id, department=user_data['department'], course=user_data['course'],
                    group_number=group_number)
        user.save()
        await state.finish()
        await message.answer("Registration complete!")