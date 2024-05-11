import unittest
from unittest.mock import patch, MagicMock
from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.commands import register, register_role, register_group_number_or_teacher_lastname, change_info, \
    change_info_new_info, Registration, ChangeInfo


class TestHandlers(unittest.TestCase):
    def setUp(self):
        self.message = types.Message(text="", from_user=types.User(id=123, is_bot=False))
        storage = MagicMock()
        storage.check_address.return_value = (MagicMock(), MagicMock())
        self.state = FSMContext(storage=storage, chat=MagicMock(), user=MagicMock())

    @patch("handlers.create_user")
    @patch("handlers.logger")
    async def test_register(self, mock_logger, mock_create_user):
        await register(self.message, self.state)
        mock_logger.info.assert_called_with("User 123 sent /register command")
        self.assertEqual(self.state.state, Registration.role)

    @patch("handlers.logger")
    async def test_register_role(self, mock_logger):
        self.message.text = "Студент"
        await register_role(self.message, self.state)
        mock_logger.info.assert_called_with("User 123 sent role: Студент")
        self.assertEqual(self.state.state, Registration.group_number_or_teacher_lastname)

    @patch("handlers.create_user")
    @patch("handlers.logger")
    async def test_register_group_number_or_teacher_lastname(self, mock_logger, mock_create_user):
        self.message.text = "12345"
        await register_group_number_or_teacher_lastname(self.message, self.state)
        mock_logger.info.assert_called_with("User 123 sent group number or teacher lastname: 12345")
        self.assertEqual(self.state.state, None)

    @patch("handlers.logger")
    async def test_change_info(self, mock_logger):
        await change_info(self.message, self.state)
        mock_logger.info.assert_called_with("User 123 sent /change_info command")
        self.assertEqual(self.state.state, ChangeInfo.new_info)

    @patch("handlers.update_user")
    @patch("handlers.logger")
    async def test_change_info_new_info(self, mock_logger, mock_update_user):
        self.message.text = "New group number"
        await change_info_new_info(self.message, self.state)
        mock_logger.info.assert_called_with("User 123 sent new info: New group number")
        self.assertEqual(self.state.state, None)

if __name__ == "__main__":
    unittest.main()
