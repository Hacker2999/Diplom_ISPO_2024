from peewee import PostgresqlDatabase, Model, IntegerField, CharField

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Подключение к базе данных PostgreSQL
db = PostgresqlDatabase(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    department = CharField()
    course = IntegerField()
    group_number = CharField()


class Schedule(BaseModel):
    group_number = CharField()
    day = CharField()
    time = CharField()
    subject = CharField()
    teacher = CharField()
    room = CharField(null=True)  # Разрешаем указание номера аудитории как необязательного


class TeacherSchedule(BaseModel):
    teacher_name = CharField()
    day = CharField()
    time = CharField()
    subject = CharField()
    group_number = CharField()
    room = CharField(null=True)


# Создание таблиц, если они не существуют
db.connect()
db.create_tables([User, Schedule, TeacherSchedule], safe=True)
