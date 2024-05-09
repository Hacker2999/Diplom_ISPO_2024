import datetime

from peewee import (
    Model, PostgresqlDatabase,
    CharField, IntegerField, ForeignKeyField, DateTimeField, BigIntegerField, TextField, CompositeKey, TimestampField
)

from config import *

db = PostgresqlDatabase(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    telegram_id = BigIntegerField(unique=True)
    username = TextField(null=True)
    first_name = TextField(null=True)
    last_name = TextField(null=True)
    department = TextField(null=True)
    course = IntegerField(null=True)
    group_number = TextField(null=True)


class Classrooms(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'Classrooms'


class Groups(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'Groups'


class Subjects(BaseModel):
    name = TextField(unique=True)

    class Meta:
        db_table = 'Subjects'


class Teachers(BaseModel):
    name = TextField(unique=True)

    class Meta:
        db_table = 'Teachers'


class Timetable(BaseModel):
    date = DateTimeField()
    lesson_number = IntegerField()
    teacherId = IntegerField(Teachers, column_name='teacherId')
    classroomId = IntegerField(Classrooms, column_name='classroomId')
    subjectId = IntegerField(Subjects, column_name='subjectId')

    class Meta:
        db_table = 'Timetable'


class GroupsToTimetable(BaseModel):
    A = ForeignKeyField(Groups, column_name='A', on_delete='CASCADE', on_update='CASCADE')
    B = ForeignKeyField(Timetable, column_name='B', on_delete='CASCADE', on_update='CASCADE')

    class Meta:
        db_table = '_GroupsToTimetable'
        primary_key = CompositeKey('A', 'B')


class TimetableEditLogs(BaseModel):
    created_at = TimestampField(default=datetime.datetime.now, null=False)
    groups = TextField(null=True)
    notify = IntegerField(default=0, null=False)

    class Meta:
        db_table = 'TimetableEditLogs'
