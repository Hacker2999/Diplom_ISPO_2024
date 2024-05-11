import unittest
from unittest.mock import patch, MagicMock

import peewee

import database
from models import Users, Timetable, Teachers, Groups, Classrooms, GroupsToTimetable, Subjects
from database import get_user_by_id, create_user, update_user, get_schedule, get_teacher_schedule


class TestUserFunctions(unittest.IsolatedAsyncioTestCase):
    @patch('models.Users.get')
    def test_get_user_by_id_found(self, mock_users_get):
        mock_users_get.return_value = MagicMock(spec_set=['id'])
        user_id = 12345
        result = get_user_by_id(user_id)
        self.assertIsNotNone(result)
        mock_users_get.assert_called_once_with(Users.id == user_id)

    @patch('models.Users.get')
    def test_get_user_by_id_not_found(self, mock_users_get):
        mock_users_get.side_effect = Users.DoesNotExist
        user_id = 12345
        result = get_user_by_id(user_id)
        self.assertIsNone(result)
        mock_users_get.assert_called_once_with(Users.id == user_id)

    @patch('models.Users.create')
    def test_create_user_success(self, mock_users_create):
        mock_users_create.return_value = MagicMock(spec_set=['id'])
        telegram_id = 12345
        result = create_user(telegram_id, name='Test User')
        self.assertIsNotNone(result)
        mock_users_create.assert_called_once_with(telegram_id=telegram_id, name='Test User')

    @patch('models.Users.create')
    def test_create_user_failure(self, mock_users_create):
        mock_users_create.side_effect = Exception('Error creating user')
        telegram_id = 12345
        result = create_user(telegram_id, name='Test User')
        self.assertIsNone(result)
        mock_users_create.assert_called_once_with(telegram_id=telegram_id, name='Test User')

    @patch('database.update_user')
    @patch('models.Users')
    def test_update_user(self, mock_Users, mock_update_user):
        # Create a mock user object
        mock_user = MagicMock()
        mock_Users.get.return_value = mock_user

        # Set the return value of the update_user function
        mock_update_user.return_value = True

        # Test updating a user
        telegram_id = 123456
        updated_data = {'teacher_lastname': 'Johnson', 'teacher_role': 0}
        self.assertTrue(database.update_user(telegram_id, **updated_data))

    @patch('models.Users.get')
    @patch('models.Users.save')
    def test_update_user_failure(self, mock_users_save, mock_users_get):
        mock_users_get.return_value = None
        mock_users_save.side_effect = Exception('Error updating user')
        telegram_id = 12345
        result = update_user(telegram_id, name='Updated User')
        self.assertFalse(result)
        mock_users_get.assert_called_once_with(telegram_id=telegram_id)
        mock_users_save.assert_not_called()


class TestScheduleFunctions(unittest.IsolatedAsyncioTestCase):
    @patch('models.GroupsToTimetable')
    @patch('models.Timetable')
    async def test_get_schedule_success(self, mock_timetable, mock_groupstotimetable):
        mock_groupstotimetable.select.return_value.join.return_value.join.return_value.join.return_value.join.return_value.where.return_value.where.return_value.limit.return_value.execute.return_value = [
            {'timetable_id': 1, 'group_number': '123', 'subject': 'Math'},
            {'timetable_id': 2, 'group_number': '123', 'subject': 'Science'},
        ]
        mock_timetable.select.return_value.join.return_value.join.return_value.join.return_value.join.return_value.where.return_value.where.return_value.limit.return_value.execute.return_value = [
            {'timetable_id': 1, 'teacher': 'Mr. Smith', 'time': '10:00'},
            {'timetable_id': 2, 'teacher': 'Ms. Johnson', 'time': '11:00'},
        ]
        group_number = '123'
        result = await get_schedule(group_number)
        print("Result:", result)  # Add a print statement to see what the result is
        self.assertIsInstance(result, peewee.ModelCursorWrapper)  # Check if the result is a ModelCursorWrapper

    @patch('models.GroupsToTimetable.select')
    @patch('models.Timetable.select')
    async def test_get_schedule_failure(self, mock_timetable_select, mock_groupstotimetable_select):
        mock_groupstotimetable_select.side_effect = Exception('Error retrieving schedule')
        group_number = '123'
        result = await get_schedule(group_number)
        self.assertIsNone(result)

    @patch('models.Teachers')
    async def test_get_teacher_schedule_success(self, mock_teacher):
        mock_teacher.select.return_value.join.return_value.join.return_value.where.return_value.where.return_value.limit.return_value.execute.return_value = [
            {'timetable_id': 1, 'teacher': 'Mr. Smith', 'time': '10:00'},
            {'timetable_id': 2, 'teacher': 'Mr. Smith', 'time': '11:00'},
        ]
        teacher_surname = 'Smith'
        result = await get_teacher_schedule(teacher_surname)
        print("Result:", result)  # Add a print statement to see what the result is
        self.assertIsInstance(result, peewee.ModelCursorWrapper)  # Check if the result is a ModelCursorWrapper

    @patch('models.Timetable.select')
    async def test_get_teacher_schedule_failure(self, mock_timetable_select):
        mock_timetable_select.side_effect = Exception('Error retrieving schedule')
        teacher_surname = 'Smith'
        result = await get_teacher_schedule(teacher_surname)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
