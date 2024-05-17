import unittest
from unittest.mock import patch, MagicMock
from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.commands import register, register_role, register_group_number, register_teacher_lastname, \
    register_teacher_select, change_info, change_info_new_info, Registration, ChangeInfo, register_button


class TestHandlers(unittest.TestCase):
    def setUp(self):
        self.message = types.Message(text="", from_user=types.User(id=123, is_bot=False))
        storage = MagicMock()
        storage.check_address.return_value = (MagicMock(), MagicMock())
        self.state = FSMContext(storage=storage, chat=MagicMock(), user=MagicMock())

    @patch("handlers.logger")
    async def test_start(self, mock_logger):
        await start(self.message)
        mock_logger.info.assert_called_with("User 123 sent /start command")

    @patch("handlers.logger")
    async def test_register_button(self, mock_logger):
        await register_button(self.message)
        mock_logger.info.assert_called_with("User 123 pressed register button")

    @patch("handlers.logger")
    async def test_register(self, mock_logger):
        await register(self.message)
        mock_logger.info.assert_called_with("User 123 sent /register command")
        self.assertEqual(self.state.state, Registration.role)

    @patch("handlers.logger")
    async def test_register_role(self, mock_logger):
        self.message.text = "Студент"
        await register_role(self.message, self.state)
        mock_logger.info.assert_called_with("User 123 sent role: Студент")
        self.assertEqual(self.state.state, Registration.group_number)

    @patch("handlers.logger")
    async def test_register_group_number(self, mock_logger):
        self.message.text = "12345"
        await register_group_number(self.message, self.state)
        mock_logger.info.assert_called_with("User 123 sent group number: 12345")
        self.assertEqual(self.state.state, None)

    @patch("handlers.logger")
    async def test_register_teacher_lastname(self, mock_logger):
        self.message.text = "Иванов"
        await register_teacher_lastname(self.message, self.state)
        mock_logger.info.assert_called_with("User 123 sent teacher lastname: Иванов")
        self.assertEqual(self.state.state, Registration.teacher_select)

    @patch("handlers.logger")
    async def test_register_teacher_select(self, mock_logger):
        self.message.text = "Иванов Иван Иванович"
        await register_teacher_select(self.message, self.state)
        mock_logger.info.assert_called_with("User 123 selected teacher: Иванов Иван Иванович")
        self.assertEqual(self.state.state, None)

    @patch("handlers.logger")
    async def test_change_info(self, mock_logger):
        await change_info(self.message, self.state)
        mock_logger.info.assert_called_with("User 123 sent /change_info command")
        self.assertEqual(self.state.state, ChangeInfo.new_info)

    @patch("handlers.logger")
    async def test_change_info_new_info(self, mock_logger):
        self.message.text = "New group number"
        await change_info_new_info(self.message, self.state)
        mock_logger.info.assert_called_with("User 123 sent new info: New group number")
        self.assertEqual(self.state.state, None)

if __name__ == "__main__":
    unittest.main()