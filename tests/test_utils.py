from unittest.mock import patch, MagicMock
from datetime import datetime
from models import Subjects, Teachers, Classrooms, GroupsToTimetable

from utils import format_schedule, format_teacher_schedule


class TestUtils:

    def test_format_schedule(self):
        with patch('models.Subjects.get') as mock_subjects_get, \
                patch('models.Teachers.get') as mock_teachers_get, \
                patch('models.Classrooms.get') as mock_classrooms_get, \
                patch('models.GroupsToTimetable.filter') as mock_groupstotimetable_filter, \
                patch('models.GroupsToTimetable.get') as mock_groupstotimetable_get:
            # Mocking database queries
            mock_subjects_get.return_value.name = "Math"
            mock_teachers_get.return_value.name = "Mr. Smith"
            mock_classrooms_get.return_value.name = "Room 101"
            mock_groupstotimetable_get.return_value.A.name = "Group 1"

            # Test data
            schedule_data = [
                MagicMock(date=datetime(2024, 5, 15), subjectId=1, teacherId=1, classroomId=1, id=1, lesson_number=1),
                MagicMock(date=datetime(2024, 5, 16), subjectId=2, teacherId=2, classroomId=2, id=2, lesson_number=2)
            ]

            result = format_schedule(schedule_data)

            expected_result = (
                ('<b>15.05/среда</b>\n'
                 '1. <b>Math</b> (Mr. Smith)\n'
                 '    каб. Room 101\n'
                 '\n'
                 '<b>16.05/четверг</b>\n'
                 '2. <b>Math</b> (Mr. Smith)\n'
                 '    каб. Room 101\n'
                 '\n')
            )

            assert expected_result in result

    def test_format_teacher_schedule(self):
        with patch('models.Subjects.get') as mock_subjects_get, \
                patch('models.Classrooms.get') as mock_classrooms_get, \
                patch('models.GroupsToTimetable.filter') as mock_groupstotimetable_filter, \
                patch('models.GroupsToTimetable.get') as mock_groupstotimetable_get:
            # Mocking database queries
            mock_subjects_get.return_value.name = "Math"
            mock_classrooms_get.return_value.name = "Room 101"
            mock_groupstotimetable_get.return_value.A.name = "Group 1"

            # Test data
            schedule_data = [
                MagicMock(date=datetime(2024, 5, 15), subjectId=1, classroomId=1, id=1, lesson_number=1),
                MagicMock(date=datetime(2024, 5, 16), subjectId=2, classroomId=2, id=2, lesson_number=2)
            ]

            result = format_teacher_schedule(schedule_data)

            # Asserts
            assert "15.05/среда" in result
            assert "Math" in result
            assert "Room 101" in result
            assert "Group 1" not in result  # Ensure "Group 1" is not in the result
